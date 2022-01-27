import shutil
import os
import glob
import socket
import traceback
import sys
import io
from dirsync import sync
from datetime import datetime

AVSHARE = 'Y:/'
AVSHARE_RECORDER_DEPLOY = os.path.join(AVSHARE, 'LATEST_RECORDING_TOOL')
AVSHARE_LOG_FN = os.path.join(AVSHARE, 'HIDDEN_FOLDERS_DONOTTOUCH', 'logs', 'update_recording_tools.txt')
LOCAL_RECORDING_TOOLS = 'C:/_Recording_Tools'
LOCAL_DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
LOCAL_LAST_UPDATED_FN = os.path.join(LOCAL_RECORDING_TOOLS, '../../../../_Recording_Tools/last_updated.txt')


def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def unzip(fn, remove=False, overwrite=True):
    import zipfile

    def get_windows_long_path(path):
        """
        If a windows path is longer than 250 characters this prefix must be added to avoid errors.
        """
        return os.path.abspath("\\\\?\\" + path)

    fn = os.path.abspath(fn)
    fn_unzipped = os.path.splitext(fn)[0]
    if overwrite and os.path.isdir(fn_unzipped):
        shutil.rmtree(fn_unzipped, ignore_errors=True)
    outdir = os.path.dirname(fn)
    if os.name == 'nt':
        outdir = get_windows_long_path(outdir)
    with zipfile.ZipFile(fn, 'r') as zip_obj:
        fns_zip = zip_obj.namelist()
        for fn_zip in fns_zip:
            zip_obj.extract(fn_zip, outdir)
    if remove:
        if os.name == 'nt':
            fn = get_windows_long_path(fn)
        os.remove(fn)


def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_shortcut(fn, target, icon_fn=None):
    ':param icon_fn: path to an .exe file from which the icon should be taken'
    import winshell
    if icon_fn:
        winshell.CreateShortcut(fn, target, Icon=(icon_fn, 0))
    else:
        winshell.CreateShortcut(fn, target)


def run():

    failure = 'No failures.'
    try:
        print('### Mounting recording drive...')
        mount_avshare_fn = os.path.join(LOCAL_RECORDING_TOOLS,
                                        '../../../../_Recording_Tools/mount_avshare_recording.bat')
        if not os.path.exists(AVSHARE_RECORDER_DEPLOY) and os.path.exists(mount_avshare_fn):
            os.system(mount_avshare_fn)

        print('### Updating mount_avshare_recording.bat...')
        src = os.path.join(AVSHARE, '../../../../_Recording_Tools/mount_avshare_recording.bat')
        dest = os.path.join(LOCAL_RECORDING_TOOLS, '../../../../_Recording_Tools/mount_avshare_recording.bat')
        try:
            shutil.copyfile(src, dest)
        except:
            print('Could not copy mount_avshare_recording from %s to %s!' % (src, dest))

        print('### Copying latest asaphus recorder...')
        latest_recorder_fns = sorted(glob.glob(os.path.join(AVSHARE_RECORDER_DEPLOY, '*_AsaphusRecorder*')))
        for fn in latest_recorder_fns:
            print('Syncing', fn)
            dest_fn = fn.replace(AVSHARE_RECORDER_DEPLOY, LOCAL_RECORDING_TOOLS)
            if fn.endswith('.zip'):
                dest_folder_unzipped = os.path.splitext(dest_fn)[0]
                if os.path.exists(dest_folder_unzipped):
                    print('Was already copied and unzipped.')
                else:
                    print('Copying...')
                    shutil.copyfile(fn, dest_fn)
                    print('Unzipping...')
                    unzip(dest_fn, remove=True)
            elif fn.endswith('.7z'):
                print('---> ERROR! 7Zip archives (ending with .7z) are not supported! Please upload recorder as .zip!')
            else:
                mkdirs(dest_fn)
                sync(fn, dest_fn, 'sync', purge=True)

        print('### Moving old recorders to _OLD subfolder...')
        mkdirs(os.path.join(LOCAL_RECORDING_TOOLS, '../../../../_Recording_Tools/_OLD'))
        local_recorder_folders = glob.glob(os.path.join(LOCAL_RECORDING_TOOLS, '*_AsaphusRecorder'))
        for folder in local_recorder_folders:
            if os.path.basename(folder) not in [os.path.splitext(os.path.basename(fn))[0]  # remove .zip extension
                                                for fn in latest_recorder_fns]:
                dest_folder = folder.replace(LOCAL_RECORDING_TOOLS, os.path.join(LOCAL_RECORDING_TOOLS,
                                                                                 '../../../../_Recording_Tools/_OLD'))
                try:
                    shutil.move(folder, dest_folder)
                except:
                    print('Could not move %s to _OLD. Probably still openend in another program.' % folder)

        print('### Updating update_recording_tools.py...')
        latest_folder = sorted(glob.glob(os.path.join(LOCAL_RECORDING_TOOLS, '*_AsaphusRecorder')))[-1]
        shutil.copyfile(os.path.join(latest_folder, 'update_recording_tools.py'),
                        os.path.join(LOCAL_RECORDING_TOOLS, 'update_recording_tools.py'))

        print('### Syncing extra folders...')
        for folder in [os.path.join(AVSHARE_RECORDER_DEPLOY, '../../../../_Recording_Tools/Optitrack Configurations'),
                       os.path.join(AVSHARE, 'ECU_FLASH_SOFTWARE',
                                    '../../../../_Recording_Tools/LATEST_ECU_FLASH_SOFTWARE'),
                       os.path.join(AVSHARE, '../../../../_Recording_Tools/WIDEANGLE-KEYS'),
                       os.path.join(AVSHARE, '../../../../_Recording_Tools/opencv_camera_calibration_binaries')]:
            print('Syncing', folder)
            dest_folder = os.path.join(LOCAL_RECORDING_TOOLS, os.path.basename(folder))
            mkdirs(dest_folder)
            sync(folder, dest_folder, 'sync', purge=True)

        print('### Creating desktop shortcut...')
        create_shortcut(os.path.join(LOCAL_DESKTOP, 'Recording_Tools.lnk'), LOCAL_RECORDING_TOOLS,
                        icon_fn=r"C:\Windows\System32\psr.exe")  # steal icon from windows steps recorder

        # write last updated
        with io.open(LOCAL_LAST_UPDATED_FN, 'w') as f:
            f.write(timestamp())

    except Exception as e:
        failure = "".join(traceback.format_exception(*sys.exc_info()))

    # write to log
    with io.open(AVSHARE_LOG_FN, 'a+') as f:
        f.write('; '.join([timestamp(), socket.gethostname(), failure]) + '\n')

    print(failure)
    input("Finished! Press enter to exit...")


if __name__ == "__main__":
    run()
    # for fn in sorted(glob.glob(os.path.join(LOCAL_RECORDING_TOOLS, '*_AsaphusRecorder'))):
    #     print(fn)
    pass
