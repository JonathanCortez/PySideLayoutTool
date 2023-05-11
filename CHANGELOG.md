## V0.3.1 (2023-05-09)
___
  - ### Added :
    - Added New Widget for Unreal Engine Plugin, replicating the unreal editor </p>
    drop-down menu for content classes and level actors.
  - ### Update :
    - Reworked the Ramp Widget to be more responsive and look to it </p>
    also added the missing interpolation types with some blends between them.
    
  - ### Hotfix : 
    - Added some small improvements to the MultiFolder(Scroll) widget </p>
    with height resize and removing item from list.

## V0.3.1 (2023-04-09)
___
  - ### Hotfix : 
    - Added `self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)` to </p>
    `class Plugin_Create(QtWidgets.QDialog):` to fix crash when closing </p>
    inside other DCC.

## V0.3.0 (2023-04-09) 
___
  - ### Feature : 
    - New **Notification** window implementation changelog view.
      - To help keep track of new updates and feature implementation for tool.
    - New functions have been added in `SetupTools.py`.
    - Create Window `?` is working now with notification window.
    - Custom plugin path.
    - New **Settings** Window has been added under **Create Button**.
      - This window will allow you to enable/disable plugins found.
    -  New system to create plugins.

  - ### Update :
    - File **UISetupModule** as been renamed to **SetupTools**
    - ` pip Markdown` has been added to install requires for pip setup.
    - Initiating **Plugins** system has been slightly reworked to be </p>
    more dynamic and easier to use.
    - `UIEditorFactory.py` func `unregister` has been updated to work with </p>
    the new **Settings > Plugins** window.
    - `SetupTools.py` has been slightly reworked to work with the new </p>
    implementation of the **Settings > Plugins** window.
    - `CreateUISetupWin.py` has been renamed to `InitWindow`.
    - `StringValidator.py` improved the special characters compile.
    - `WindowsManager.py` has been renamed to `WindowsModule`.
    - `README.md` has been updated to reflect the new **Plugins** system and tool usage.
    - `SetupTools.py` new functions.
        - `set_custom_plugin_loader(plugin_path: str) -> None`
        - `load_plugin_modules(plugin_name : str, path : str) -> None`
        - `unload_plugin_modules(plugin_name : str, path : str) -> None`
        - `Tool_Json_Data() -> tuple`
        - `enable_notification(state: bool) -> None`

  - ### Added :
    - New **Plugins** system.
    - New **Settings** window.
    - New **Notification** window.
    - New **Create Plugins** window
    - Documentation for **Plugins** system has been added.