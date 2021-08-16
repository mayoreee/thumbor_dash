[watcher:thumbor_dash]
cmd = python
args = -m thumbor_dash/server --conf=/app/thumbor.conf --fd $(circus.sockets.thumbor_dash) -l {{ LOG_LEVEL | default("info") }}

use_sockets = True
working_dir = /app
copy_env = True
autostart = True

[socket:thumbor_dash]
host = 0.0.0.0
port = {{ THUMBOR_PORT | default(80) }}