from PySideLayoutTool.UIEditorLib.UIEditorIconFactory import IconEditorFactory

def register() -> None:
    resource_path = '/PySideLayoutTool/resources/images'

    IconEditorFactory.register('folder_nor', f'{resource_path}/normal_folder.svg')
    IconEditorFactory.register('folder_add', f'{resource_path}/folder_add.svg')
    IconEditorFactory.register('folder_sub', f'{resource_path}/folder_minus.svg')

    IconEditorFactory.register('lock_open', f'{resource_path}/lock_unlocked.svg')
    IconEditorFactory.register('lock_closed', f'{resource_path}/lock_locked.svg')

    IconEditorFactory.register('splitter_v1', f'{resource_path}/vertical_alt.svg')
    IconEditorFactory.register('splitter_v2', f'{resource_path}/splitter_vertical_alt_2.svg')

    IconEditorFactory.register('separtor_v1', f'{resource_path}/border_style_dashed_sep.svg')
    IconEditorFactory.register('separtor_v2', f'{resource_path}/border_style_solid_sep.svg')

    IconEditorFactory.register('arrow_v1_right', f'{resource_path}/chevron_arrow_right.svg')
    IconEditorFactory.register('arrow_v1_down', f'{resource_path}/chevron_arrow_down.svg')

    IconEditorFactory.register('unchecked', f'{resource_path}/checkbox_unchecked.svg')
    IconEditorFactory.register('checked', f'{resource_path}/checkbox_checked.svg')

    IconEditorFactory.register('eye_v1', f'{resource_path}/eye_view.svg')

    IconEditorFactory.register('move_right', f'{resource_path}/move_right_arrow.svg')
    IconEditorFactory.register('move_left', f'{resource_path}/move_left_arrow.svg')

    IconEditorFactory.register('comment', f'{resource_path}/comment.svg')

    IconEditorFactory.register('zoom_In',f'{resource_path}/zoom_in.svg')
    IconEditorFactory.register('zoom_Out', f'{resource_path}/zoom_out.svg')

    IconEditorFactory.register('add_file', f'{resource_path}/add_file.svg')

    IconEditorFactory.register('arrow_exchange_alt', f'{resource_path}/arrow_exchange_alt.svg')
    IconEditorFactory.register('arrow_exchange_v', f'{resource_path}/arrow_exchange_v.svg')

    IconEditorFactory.register('arrow_open', f'{resource_path}/arrow_chevron_up.svg')
    IconEditorFactory.register('arrow_close', f'{resource_path}/arrow_chevron_down.svg')

    IconEditorFactory.register('menu_list', f'{resource_path}/menu_list_display.svg')

