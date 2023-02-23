def write_ceritficate(name_file_pem,data_pem):
    f =  open(f"src/certificates/{name_file_pem}.pem","w")
    f.write(data_pem)
    f.close()
    