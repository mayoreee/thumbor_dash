from datetime import datetime
from json import dumps, loads

from thumbor_dash.storages.request_storage import RequestStorage
from thumbor_dash.utils import datetimeToMillisecondsSinceEpoch


async def verify_user_access_status(requester_id, config):
    """
    Checks the requester's ban status and updates their access information.

    Parameters:
        requester_id (str): The ID of the requester.
        config (object): Configuration object containing limits and durations.

    Returns:
        bool: True if the user has access, False if banned.
    """
    # Convert time limits from minutes to milliseconds
    REQUEST_TIME_LIMIT = config.REQUEST_TIME_LIMIT * 60 * 1000
    USAGE_VIOLATION_LIMIT = config.USAGE_VIOLATION_LIMIT
    BAN_DURATION = config.BAN_DURATION * 60 * 1000

    storage = RequestStorage()
    storage_get_result = await storage.get(requester_id=requester_id)

    current_time = datetimeToMillisecondsSinceEpoch(datetime.now())

    if storage_get_result is None:
        # First-time requester, initialize their data
        await update_requester_data(
            requester_id=requester_id,
            storage=storage,
            is_banned=False,
            last_accessed=current_time,
            usage_violation_count=0,
            next_access=0
        )
        return True

    else:
        # Load existing requester data
        requester_data = loads(storage_get_result)
        is_banned = requester_data['is_banned']
        last_accessed = requester_data['last_accessed']
        usage_violation_count = requester_data['usage_violation_count']
        next_access = requester_data['next_access']

        time_since_last_access = current_time - last_accessed

        if not is_banned:
            if time_since_last_access < REQUEST_TIME_LIMIT:
                usage_violation_count += 1
            else:
                # Reset violation count after time limit has passed
                usage_violation_count = 1

            if usage_violation_count > USAGE_VIOLATION_LIMIT:
                is_banned = True
                next_access = current_time + BAN_DURATION

        if is_banned:
            if current_time >= next_access:
                # Ban period is over, reset data
                is_banned = False
                usage_violation_count = 0
                next_access = 0
                access_granted = True
            else:
                # User is still banned
                access_granted = False
        else:
            access_granted = True

        # Update requester data
        await update_requester_data(
            requester_id=requester_id,
            storage=storage,
            is_banned=is_banned,
            last_accessed=current_time,
            usage_violation_count=usage_violation_count,
            next_access=next_access
        )

        return access_granted


async def update_requester_data(requester_id, storage, is_banned, last_accessed, usage_violation_count, next_access):
    """
    Updates the requester data in storage.

    Parameters:
        requester_id (str): The ID of the requester.
        storage (RequestStorage): The storage object.
        is_banned (bool): Ban status of the requester.
        last_accessed (int): The last accessed timestamp in milliseconds.
        usage_violation_count (int): Number of usage violations.
        next_access (int): Timestamp when the requester can access again.
    """
    requester_data = {
        'is_banned': is_banned,
        'last_accessed': last_accessed,
        'usage_violation_count': usage_violation_count,
        'next_access': next_access  # Next time the user gets access after a ban
    }
    file_bytes = dumps(requester_data).encode('utf-8')
    await storage.put(requester_id=requester_id, file_bytes=file_bytes)
