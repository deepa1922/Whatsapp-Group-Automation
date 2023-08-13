# Before running this script, please refer to the documentation (documentation.txt) for important ethical considerations and policy adherence.

from GroupAutomation import setup_driver,wait_for_qr_scan, add_participants , create_group,send_message
def main():
    try:
        #setup the driver
        driver = setup_driver()

        #wait for QR code scan
        wait_for_qr_scan(driver)


        participants = ["contact1","contact2"]
        group_name =["Group"]

        #create the group
        create_group(driver,participants,group_name)
        print("Group Created Successfully")

        # Call the function to send a message
        group_name = "Group"
        message = "Hello, this is a test message!"
        send_message(driver, group_name, message)
        print("message sent successfully")

        #close the driver
        driver.quit()
    except Exception as e:
       print("An error occurred ", str(e))

if __name__ == "__main__":
    main()
