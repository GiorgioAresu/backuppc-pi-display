BACKUPPC_DIR = "/usr/share/backuppc"
TARGET_HOST = "192.168.1.65"
BACKUPPC_USER_UID = 110
BACKUPPC_USER_GID = 116
DEBUG = False

TRANSLATIONS = {
    'Status_idle': 'inattivo',
    'Status_backup_starting': 'avvio backup',
    'Status_backup_in_progress': 'backup in esecuzione',
    'Status_restore_starting': 'avvio ripristino',
    'Status_restore_in_progress': 'restore in esecuzione',
    'Status_link_pending': 'collegamenti pendenti',
    'Status_link_running': 'collegamenti in esecuzione',
    'Reason_backup_done': 'backup eseguito',
    'Reason_restore_done': 'restore eseguito',
    'Reason_archive_done': 'archivio eseguito',
    'Reason_nothing_to_do': 'nulla da fare',
    'Reason_backup_failed': 'backup fallito',
    'Reason_restore_failed': 'restore fallito',
    'Reason_archive_failed': 'archivio fallito',
    'Reason_no_ping': 'no ping',
    'Reason_backup_canceled_by_user': 'backup annullato dall\'utente',
    'Reason_restore_canceled_by_user': 'ripristino annullato dall\'utente',
    'Reason_archive_canceled_by_user': 'archivio annullato dall\'utente',
    'Disabled_OnlyManualBackups': 'auto disabilitato',
    'Disabled_AllBackupsDisabled': 'disabilitato',
    'full': 'completo',
    'incr': 'incrementale',
    'backupType_partial': 'parziale',
}