'''
задание python:
1. я програмно задаю название папок(пусть это будет масив с папками). Те папки что есть в масиве нужно удалить на моем гугл драйве.
усложнение: сделать 2 массива в одном я задаю название папок которые будут удаляться, во 2-м массиве я
задаю название папок в котором будут удаляться только ФАЙЛЫ не папки
библиотеки для работы с гугл драйвом: pydrive
'''
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class DriveFolder:
    i = 0
    filesName = ['file1.txt','file2.txt','file3.txt','file3.txt','file4.txt','file5.txt']  # for CreateFiles() #TODO
    objectsToDelete = ['Folder1']
    driveFilesCouter = len(objectsToDelete)

    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication. // Аунтификация
        self.drive = GoogleDrive(gauth)  # Create GoogleDrive instance with authenticated GoogleAuth instance

    def GetFilesList(self):  # //Возвращает список файлов на диске
        # Auto-iterate through all files that matches this query
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    def CreateFolders(self):  # Create folder //Создание папок на диске
        foldersName = ['Folder1', 'Folder2', 'Folder3', 'Folder4', 'Folder5']
        array_couter = len(foldersName)
        folderid = ''
        for i in range(array_couter):
            foldertest = foldersName[i]
            try:
                folder_metadata = {'title': foldertest, 'mimeType': 'application/vnd.google-apps.folder'}
                folder = self.drive.CreateFile(folder_metadata)
                folder.Upload()
                self.folderid = folder['id']
                self.CreateFiles(self.folderid)
            except IndexError:
                print("Array error in CreateFoldersonDrive")

    def CreateFiles(self, folderid):  # Создание и загрузка файла в текущуюю папку
        file1 = self.drive.CreateFile(
            {"title": self.filesName[self.i], "parents": [{"kind": "drive#fileLink", "id": self.folderid}]})
        file1.SetContentString('Hello World!')
        file1.Upload()  # Upload the file.
        self.i = self.i + 1

    def DeleteFolders(self):
        j = 0
        for file_list in self.drive.ListFile({'q': 'trashed=false', 'maxResults': 1000}):
            #print('Received %s files from Files.list()' % len(file_list))
            for file1 in file_list:
                #print('title: %s, id: %s' % (file1['title'], file1['id']))
                #print(file1['title'] + " " + self.objectsToDelete[j])
                if file1['title'] in self.objectsToDelete:
                    file1.Delete()
                    print('title: %s, id: %s' % (file1['title'], file1['id']))
                    print('has been delete')
                else:
                    if j >= self.driveFilesCouter:
                        j = 0





# CALL'S
DriveQuery1 = DriveFolder()
#DriveQuery1.GetFilesList()
DriveQuery1.DeleteFolders() #Удаление файлов
#DriveQuery1.CreateFolders() #Создание папок и файлов
#DriveQuery1.CreateFiles() прописан в CreateFolders() (не вызывать)
#DriveQuery1.GetFilesList()
