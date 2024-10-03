from thumbor_dash.storages.request_storage import RequestStorage
from json import dumps, loads
from datetime import datetime
from thumbor_dash.utils import datetimeToMillisecondsSinceEpoch



async def verifyUserAccessStatus(requester_id, config):
    ''' Checks requester's ban status '''
    REQUEST_TIME_LIMIT = config.REQUEST_TIME_LIMIT * 60 * 1000 #convert minutes to milliseconds
    USAGE_VIOLATION_LIMIT = config.USAGE_VIOLATION_LIMIT 
    BAN_DURATION = config.BAN_DURATION * 60 * 1000 #convert minutes to milliseconds

    storage = RequestStorage()
    storage_get_result = await storage.get(requester_id=requester_id)
 
    if storage_get_result is None:
        storage_put_result = await update_requester_data(requester_id=requester_id, storage=storage, is_banned=False, last_accessed=datetimeToMillisecondsSinceEpoch(datetime.now()), usage_violation_count=0, next_access=0)
        return True
    else:
        requester_storage_data = loads(storage_get_result)
  
        is_banned = requester_storage_data['is_banned']
        last_accessed = requester_storage_data['last_accessed']
        usage_violation_count = requester_storage_data['usage_violation_count']
        next_access = requester_storage_data['next_access']

        current_time = datetimeToMillisecondsSinceEpoch(datetime.now())
        
        if ((current_time - last_accessed) < REQUEST_TIME_LIMIT) and is_banned==False:
            usage_violation_count = usage_violation_count + 1

        if (usage_violation_count > USAGE_VIOLATION_LIMIT) and is_banned==False:
            is_banned = True
            next_access = current_time + BAN_DURATION

        if is_banned:
            if next_access <= current_time:
                is_banned = False
                usage_violation_count = 0
                storage_put_result = await update_requester_data(requester_id=requester_id, storage=storage, is_banned=is_banned, last_accessed=current_time, usage_violation_count=usage_violation_count, next_access=next_access)
                return True
            else:   
                storage_put_result = await update_requester_data(requester_id=requester_id, storage=storage, is_banned=is_banned, last_accessed=current_time, usage_violation_count=usage_violation_count, next_access=next_access)
                return False
            
        storage_put_result = await update_requester_data(requester_id=requester_id, storage=storage, is_banned=is_banned, last_accessed=current_time, usage_violation_count=usage_violation_count, next_access=next_access)
        return True
        

async def update_requester_data(requester_id, storage, is_banned, last_accessed, usage_violation_count, next_access):
    requester_data = {
        'is_banned': is_banned,
        'last_accessed': last_accessed,
        'usage_violation_count': usage_violation_count,
        'next_access': next_access # next time a user gets access after a ban
        }
    file_bytes = dumps(requester_data).encode('utf-8')
    storage_put_result = await storage.put(requester_id=requester_id, file_bytes=file_bytes)   


