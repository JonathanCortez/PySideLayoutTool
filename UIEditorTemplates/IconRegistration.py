from PySideLayoutTool.UIEditorLib.UIEditorIconFactory import IconEditorFactory
from PySide2.QtGui import QIcon, QKeySequence, QPixmap


def register() -> None:
    resource_path = ':/Resources/Icons'

    IconEditorFactory.register('folder_nor', QIcon(QPixmap(f'{resource_path}/normal_folder.svg')))
    IconEditorFactory.register('folder_add', QIcon(QPixmap(f'{resource_path}/folder_add.svg')))
    IconEditorFactory.register('folder_sub', QIcon(QPixmap(f'{resource_path}/folder_minus.svg')))

    IconEditorFactory.register('lock_open', QIcon(QPixmap(f'{resource_path}/lock_unlocked.svg')))
    IconEditorFactory.register('lock_closed', QIcon(QPixmap(f'{resource_path}/lock_locked.svg')))

    IconEditorFactory.register('splitter_v1', QIcon(QPixmap(f'{resource_path}/vertical_alt.svg')))
    IconEditorFactory.register('splitter_v2', QIcon(QPixmap(f'{resource_path}/splitter_vertical_alt_2.svg')))

    IconEditorFactory.register('separtor_v1', QIcon(QPixmap(f'{resource_path}/border_style_dashed_sep.svg')))
    IconEditorFactory.register('separtor_v2', QIcon(QPixmap(f'{resource_path}/border_style_solid_sep.svg')))

    IconEditorFactory.register('arrow_v1_right', QIcon(QPixmap(f'{resource_path}/chevron_arrow_right.svg')))
    IconEditorFactory.register('arrow_v1_down', QIcon(QPixmap(f'{resource_path}/chevron_arrow_down.svg')))

    IconEditorFactory.register('unchecked', QIcon(QPixmap(f'{resource_path}/checkbox_unchecked.svg')))
    IconEditorFactory.register('checked', QIcon(QPixmap(f'{resource_path}/checkbox_checked.svg')))

    IconEditorFactory.register('eye_v1', QIcon(QPixmap(f'{resource_path}/eye_view.svg')))

    IconEditorFactory.register('move_right', QIcon(QPixmap(f'{resource_path}/move_right_arrow.svg')))
    IconEditorFactory.register('move_left', QIcon(QPixmap(f'{resource_path}/move_left_arrow.svg')))

    IconEditorFactory.register('comment', QIcon(QPixmap(f'{resource_path}/comment.svg')))

    IconEditorFactory.register('zoom_In',QIcon(QPixmap(f'{resource_path}/zoom_in.svg')))
    IconEditorFactory.register('zoom_Out', QIcon(QPixmap(f'{resource_path}/zoom_out.svg')))

    IconEditorFactory.register('add_file', QIcon(QPixmap(f'{resource_path}/add_file.svg')))

    IconEditorFactory.register('arrow_exchange_alt', QIcon(QPixmap(f'{resource_path}/arrow_exchange_alt.svg')))
    IconEditorFactory.register('arrow_exchange_v', QIcon(QPixmap(f'{resource_path}/arrow_exchange_v.svg')))

    IconEditorFactory.register('arrow_open', QIcon(QPixmap(f'{resource_path}/arrow_chevron_up.svg')))
    IconEditorFactory.register('arrow_close', QIcon(QPixmap(f'{resource_path}/arrow_chevron_down.svg')))

    IconEditorFactory.register('menu_list', QIcon(QPixmap(f'{resource_path}/menu_list_display.svg')))

