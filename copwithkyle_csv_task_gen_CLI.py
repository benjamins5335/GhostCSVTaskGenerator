import csv
import math

def get_sku():
    sku = input("What is the sku of the shoe? (in format 'XXXXXX-XXX')")
    return sku

def accounts_gen():
    accounts = []
    p=open("ghostaccounts.txt","r")
    accounts = p.readlines()
    no_accounts = len(accounts)
    for index in range(no_accounts):
        accounts[index] = accounts[index].strip("\n")

    return no_accounts, accounts

def proxy_gen():
    p = open("ghostproxies.txt","r")
    proxies = p.readlines()
    no_proxies = len(proxies)
    for index in range(no_proxies):
        proxies[index] = proxies[index].strip("\n")

    return proxies, no_proxies

def profile_gen(no_proxies,no_accounts):
    card_acc_ratio = int(input("How many accounts would you like to run per profile?"))
    profiles_array =[]
    rdm_apts = []
    rdm_names = []
    rdm_phones = []
    p=open("ghostprofiles.txt","r")
    profiles = p.readlines()
    no_tasks = len(profiles)*card_acc_ratio
    maximum = assess_max(no_proxies,no_tasks,no_accounts)
    no_profiles = 0
    remainder_profiles_wrote = 0
    limit = math.ceil(maximum/len(profiles))
    pro_remainder = (limit*len(profiles))-maximum
    for index in range(len(profiles)):
        profiles[index]=profiles[index].strip("\n")
    
        rdm_apt = input("Would you like the profile: '" + profiles[index] + "' to have a random apartment? Type 'y' or 'n'...")
        rdm_name = input("Would you like the profile: '" + profiles[index] + "' to have a random name? Type 'y' or 'n'...")
        rdm_phone = input("Would you like the profile: '" + profiles[index] + "' to have a random phone number? Type 'y' or 'n'...")
        print("")
        limit = math.ceil(maximum/len(profiles))
        if remainder_profiles_wrote < pro_remainder:
            limit = limit - 1
            remainder_profiles_wrote = remainder_profiles_wrote + 1
        for counter in range(limit):
            profiles_array.append(1)
            rdm_apts.append(1)
            rdm_names.append(1)
            rdm_phones.append(1)

            profiles_array[no_profiles] = profiles[index]
 
            if rdm_apt == "y":
                rdm_apts[no_profiles] = "true"
            else:
                rdm_apts[no_profiles] = "false"
            if rdm_name == "y":
                rdm_names[no_profiles] = "true"
            else:
                rdm_names[no_profiles] = "false"
            if rdm_phone == "y":
                rdm_phones[no_profiles] = "true"
            else:
                rdm_phones[no_profiles] = "false"
            
            no_profiles = no_profiles + 1
            
    return no_profiles, profiles_array, rdm_apts, rdm_names, rdm_phones, maximum

def assess_max(no_proxies,no_tasks,no_accounts):
    print("There are " + str(no_proxies) + " proxies available, " + str(no_tasks) + " tasks able to be used by by the profiles, and " + str(no_accounts) + " accounts available")
    maximum = no_proxies
    if no_tasks < maximum:
        maximum = no_tasks
    if no_accounts < maximum:
        maximum = no_accounts
    print("So the maxiumum number of tasks you can create is " + str(maximum))
    return maximum
  
def size_run_gen(maximum):
    init_size = float(input("What is the starting size of the size run you would like to run for?"))
    end_size = float(input("What is the ending size of the size run you would like to run for?"))
    size_array = []
    nth_acc = 0
    no_sizes = (((end_size-init_size)*2)+1)
    accs_per_size_rounded = int(round(maximum/no_sizes))
    current_size = init_size
    
    remainder_mode, remainder = find_remainder(maximum,accs_per_size_rounded,no_sizes)
    remainder_accs_made= 0
    while current_size<=end_size:
        limit = accs_per_size_rounded
        if remainder_accs_made < remainder:
            if remainder_mode == "more":
                limit = limit + 1
            if remainder_mode == "less":
                limit = limit - 1
            remainder_accs_made = remainder_accs_made + 1
            
        str_current_size = str(current_size)
        for counter in range(limit):
            if nth_acc < maximum:
                size_array.append(1)
                    
                if ".0" in str_current_size:
                    if str_current_size.strip(".0") == "1":
                        str_current_size = "10"
                        size_array[nth_acc] = str_current_size
                    else:
                        size_array[nth_acc] = str_current_size.strip(".0")
                else:
                    size_array[nth_acc] = str_current_size
            
                nth_acc = nth_acc + 1
                
        current_size=current_size + 0.5

    return size_array

def find_remainder(maximum,accs_per_size_rounded,no_sizes):
    remainder = maximum - (accs_per_size_rounded*no_sizes)
    if remainder < 0:
        remainder = remainder * -1
        remainder_mode = "less"
    elif remainder > 0:
        remainder_mode = "more"
    else:
        remainder_mode = None
    return remainder_mode, remainder

def write_to_csv(maximum):
    print("Writing " + str(maximum) + " tasks to csv file...")
    with open('ghost_tasks.csv','w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['URL','Size','Proxy','Account','Profile','Random Apt','Random Name','Random Phone'])
        for index in range(maximum):
            csvwriter.writerow([sku, size_array[index],proxies[index],accounts[index],profiles_array[index],rdm_apts[index],rdm_names[index],rdm_phones[index]])


sku = get_sku()
no_accounts, accounts = accounts_gen()
proxies, no_proxies = proxy_gen()
no_profiles, profiles_array, rdm_apts, rdm_names, rdm_phones, maximum = profile_gen(no_proxies,no_accounts)
size_array = size_run_gen(maximum)
write_to_csv(maximum) 

close = input("Successfully created csv file! Press enter to exit")
quit
