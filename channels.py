from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from utils import get_numeric_files_level, get_numeric_files
import io
import json
from googleapiclient.errors import HttpError

class Channels():

    def __init__(self, drive):
        self.drive = drive

    def make(self):
        head = True
        #head_block = get_numeric_files()

        branches = []

        while (True):
            if (head):
                #files = self.drive.files().list().execute().get('files', [])
                head_block = self.get_head()
                count = 0
                position_in_chain = 0
                #print(head_block)
                level = head_block['number']
                self.favorite_files(head_block['file']['id'])
                blockDic = self.download_block(head_block['file']['id'])
                blockDic['id'] = head_block['file']['id']
                branches.append(blockDic)
                #print(branches)
                while (level >= 0):
                    level -= 1
                    blocks_level = self.get_files_level(level)
                    blocksTMP = []
                    print(blocks_level)
                    for i in blocks_level:
                        print("BLOCO PROCESSADO: ")
                        print(i)
                        blockDic_TMP = self.download_block(i['id'])
                        blockDic_TMP['id'] = i['id']
                        blocksTMP.append(blockDic_TMP)
                        print("saiu do IF:")

                    hash_goal = branches[position_in_chain]['previous_hash']
                    print(hash_goal)
                    for i in blocksTMP:
                        print("VERIFICAÇÃO DE HASH: ")
                        print(i)
                        if (i['hash'] == hash_goal):
                            print("Adicionei:")
                            print(i)
                            self.favorite_files(i['id'])
                            branches.append(i)
                            position_in_chain += 1
                            break
                '''for i in head_block:
                    print(i)
                    branches.insert(count, self.download_block(i['id']))
                    count+=1
                print(branches)'''
                print(branches)
                self.save_chan_one(branches)
                break
                   
    def save_chan_one(self, chan):
        with open("chan01.txt", "w") as file:
            json.dump(chan, file, indent=4)
            #file.writelines(chan)


    def download_block(self, id):
        request = self.drive.files().get_media(fileId=id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False    
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)  # Volta para o início do arquivo
        content = file_stream.read().decode("utf-8")  # Decodifica para string

        ## Converter arquivo txt para dicionario
        contentDict = json.loads(content)
        # self.favorite_files(contentDict)
        return contentDict

    def favorite_files(self, file_id):
        print(f"Favoritando arquivo: {file_id}")

        try:
            self.drive.files().update(  # Usando 'self.drive_service'
                fileId=file_id,
                body={"starred": True}
            ).execute()
            print(f"Arquivo {file_id} favoritado com sucesso!")
        except HttpError as error:
            print(f"Erro ao favoritar arquivo {file_id}: {error}")

    def get_files_level(self, level):
        
        files = self.drive.files().list().execute().get('files', [])

        return get_numeric_files_level(files, int(level))

    def get_head(self):
        head = self.drive.files().list(
            pageSize=10,  
            fields="files(id, name, createdTime)",
            orderBy="createdTime desc"  
        ).execute().get('files', [])

        head_block = get_numeric_files(head)

        #head_number = (max(head, key=lambda x: x['name'])['name']).split('.')[0]

        return head_block
