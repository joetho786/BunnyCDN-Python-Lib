

'''This code is to use the BunnyCDN Storage API'''


import requests
from requests.exceptions import HTTPError
from requests.models import Response
from requests.sessions import default_headers



class Storage():
    #initializer for storage account
    def __init__(self,api_key,storage_zone,storage_zone_region='de'):
        '''
        Creates an object for using BunnyCDN Storage API
        Parameters
        ----------
        api_key                                 : String
                                                  Your bunnycdn storage Api_key/FTP password of storage zone
        storage_zone                            : String
                                                  Name of your storage zone
        storage_zone_region(optional parameter) : String
                                                  The storage zone region code as per BunnyCDN (ex:Singapore region code is 'sg')
        '''
        self.headers={
            #headers to be passed in HTTP requests
            'AccessKey':api_key,
            'Content-Type':'application/json',
            'Accept':'applcation/json'
        }
        
        assert storage_zone !='',"storage_zone is not specified/missing" #applying constraint that storage_zone must be specified
        
        #For generating base_url for sending requests
        if (storage_zone_region == 'de' or storage_zone_region == ''):
            self.base_url = 'https://storage.bunnycdn.com/'+storage_zone+'/'
        else:
            self.base_url = 'https://'+storage_zone_region+'.storage.bunnycdn.com/'+storage_zone+'/'
    


    def GetStorageZoneFile(self,storage_path,download_path=None):
            '''
            This function will get the files and subfolders of storage zone mentioned in path and download it to the download_path location mentioned
                        
            Parameters
            ----------
            storage_path  : String
                            The path of the directory(including file name and excluding storage zone name) from which files are to be retrieved
            download_path : String
                            The directory on local server to which downloaded file must be saved 
            Note:For download_path instead of '\' '\\' should be used example: C:\\Users\\XYZ\\OneDrive
            '''
           
            assert storage_path !='',"storage_path must be specified"          #to make sure storage_path is not null
            #to build correct url
            if storage_path[0]=='/':
                storage_path=storage_path[1:]
            if storage_path[-1]=='/' :
                url=self.base_url+storage_path[:-1]
            else:
                url=self.base_url+storage_path
            
            file_name=url.split('/')[-1]              #For storing file name 
            
            
            #to return appropriate help messages if file is present or not and download file if present
            try:
                response=requests.get(url,headers=self.headers,stream=True)
                response.raise_for_status()
            except HTTPError as http:
                print(f'HTTP Error occured: {http}')
            except Exception as err:
                print(f"Error Occured:{err}")
            else:
                if download_path==None:
                    download_path=file_name
                else:
                    download_path+='\\' + file_name
                
                #Downloading file
                with open(download_path,'wb') as file:
                    
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                    print("File downloaded Successfully")
            
            
    
    def PutFile(self,file_name,local_upload_file_path=None,storage_path=''):

            '''
            This function uploads files to your BunnyCDN storage zone
            
            Parameters
            ----------
            storage_path                : String
                                        The path of directory in storage zone to which file is to be uploaded
            file_name                   : String
                                        The name of the file with which it is to be selected from the local directory of the device
            local_upload_file_path      : String
                                        The path of file as stored in local server from where we upload to BunnyCDN storage
            '''
            if local_upload_file_path==None:
                local_upload_file_path==file_name
            else:
                local_upload_file_path=local_upload_file_path+'\\'+file_name

            assert storage_path !='',"storage_path must be specified"   #to make sure storage_path is not null
                #to build correct url
            if storage_path[0]=='/':
                storage_path=storage_path[1:]
            if storage_path[-1]=='/' :
                url=self.base_url+storage_path[:-1]
            else:
                url=self.base_url+storage_path
            with open(local_upload_file_path,'rb') as file:
                file_data=file.read()

            response=requests.put(url,data=file_data,headers=self.headers)
            try:
                response.raise_for_status()
            except HTTPError as http:
                print("Upload Failed")
                print(f'HTTP Error Occured: {http}')
            else:
                print("The File Upload was Successful")
                

    def DeleteFile(self,storage_path=''):
            '''
            This function deletes a file mentioned in the storage_path from the storage zone

            Parameters
            ----------
            storage_path : The directory path to your file(including file name) which is to be deleted.
                        If this is the root of your storage zone, you can ignore this parameter.
            '''
            #Add code below
            assert storage_path !='',"storage_path must be specified"#to make sure storage_path is not null
            #to build correct url
            if storage_path[0]=='/':
                storage_path=storage_path[1:]
            if storage_path[-1]=='/' :
                url=self.base_url+storage_path[:-1]
            else:
                url=self.base_url+storage_path
            
            response=requests.delete(url,headers=self.headers)
            try:
                response.raise_for_status
            except HTTPError as http:
                print(f'HTTP Error occured: {http}')
                print('Object Delete failed ')
            else:
                print("Object Successfully Deleted")

   

    def Get_Storaged_Objects_List(self,storage_path=''):
            '''
            This functions returns a list of files and directories located in given storage_path.

            Parameters
            ----------
            storage_path : The directory path that you want to list.
            '''
            #Add code below
            assert storage_path !='',"storage_path must be specified"#to make sure storage_path is not null
            #to build correct url
            if storage_path[0]=='/':
                storage_path=storage_path[1:]
            if storage_path[-1]!='/' :
                url=self.base_url+storage_path+'/'
            else:
                url=self.base_url+storage_path
            try:
                response=requests.get(url,headers=self.headers)
                response.raise_for_status()
            except HTTPError as http:
                print(f'http error occured {http}')
            else:
                storage_list=[]
                for dictionary in response.json():
                    z={}
                    for key in dictionary:
                        if key == 'ObjectName' and dictionary['IsDirectory']==False:
                            z['File_Name']=dictionary[key]
                        if key == 'ObjectName' and dictionary['IsDirectory']:
                            z['Folder_Name']=dictionary[key]
                    storage_list.append(z)
                print('A List of Objects')
                return storage_list