from subprocess import check_output

vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
fn_tmp = r"C:\Users\Phan\Downloads\20220131_97053079_135416.avi"

check_output('"%s" %s' % (vlc_path, fn_tmp), shell=True)


