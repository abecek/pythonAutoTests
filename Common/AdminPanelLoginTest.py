from selenium import webdriver
from Common import Config

import time
from selenium.webdriver.common.keys import Keys

base_url = 'http://192.168.33.111/'
adminpanel_suffix = 'admin'
admin_login = 'selenium-admin'
admin_pass = 'admin123'

login_username_input_id = 'username'
login_password_input_id = 'login'
login_submit_btn_class = 'action-login'
adminpanel_dashboard_h1_class_name = 'page-title'
adminpanel_dashboard_h1_text_value = 'Dashboard'

drivers = [
    webdriver.Chrome(r'C:\dev\PRIORITIES\selenium-project\drivers\chromedriver.exe'),
    #webdriver.Firefox(executable_path=r'C:\dev\PRIORITIES\selenium-project\drivers\geckodriver.exe'),
    #webdriver.Ie(r'C:\dev\PRIORITIES\selenium-project\drivers\IEDriverServer.exe'),
]

#System.setProperty("webdriver.ie.driver", "\\IEDriverServer.exe path");
#DesiredCapabilities capabilities = DesiredCapabilities.internetExplorer();
#capabilities.setCapability(CapabilityType.ACCEPT_SSL_CERTS, true);

for driver in drivers:

    driver.set_page_load_timeout(45)
    driver.maximize_window()
    driver.get(base_url + adminpanel_suffix)
    time.sleep(5)
    
    while driver.find_element_by_id(login_username_input_id).is_displayed() == False:
        time.sleep(5)

    username_input = driver.find_element_by_id(login_username_input_id)
    username_input.send_keys(admin_login)

    while driver.find_element_by_id(login_password_input_id) == False:
        time.sleep(5)

    password_input = driver.find_element_by_id(login_password_input_id)
    password_input.send_keys(admin_pass)

    while driver.find_element_by_class_name(login_submit_btn_class).is_displayed() == False:
        time.sleep(5)

    submit_btn = driver.find_element_by_class_name(login_submit_btn_class)
    submit_btn.send_keys(Keys.ENTER)
    time.sleep(5)

    counter = 0
    while driver.find_element_by_class_name(adminpanel_dashboard_h1_class_name).is_displayed() == False:
        # todo: currently not working
        #if driver.find_element_by_class_name('action-close').is_displayed() == True:
        #    print('ESCAPE executed')
        #    driver.find_element_by_class_name('action-close').send_keys(Keys.ESCAPE)
        time.sleep(5)
        counter += 1
        if counter == 7:
            print('Test failed!')

    page_title = driver.find_element_by_class_name(adminpanel_dashboard_h1_class_name)
    if page_title.text == adminpanel_dashboard_h1_text_value:
        print('Successfully completed test!')

print('Starting SSH tests...')
from Connections import Ssh
file_name = 'FAVLIST_20180916110017'
local_path = '../Files/Import/'
remote_path = Config.Config.webroot_path + 'var/import/molsoncoors/uk/Wishlist/'
driver = drivers[0]

ssh_cl = Ssh.SshClient()
ssh_client = ssh_cl.connect()

print('Preparing adapters...')
ssh_cl.execute_adapter_reset(ssh_client)
print('Adapters are ready.')

print("Starting file transfer from: " + local_path + file_name + ' to: ' + remote_path + file_name)
ssh_cl.transfer_file(ssh_client, local_path + file_name, remote_path + file_name)
print('File transfer is done.')

print('Checking is file transferred...')
fileTransferred = ssh_cl.check_is_file_tansferred(ssh_client, remote_path, file_name)
if fileTransferred:
    print('File "' + file_name + '" properly transferred to: ' + remote_path)
else:
    print('File transfer failed.')

print('SSH tests finished...')

driver.quit()
