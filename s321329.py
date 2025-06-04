class ExamException(Exception) :
    pass

class CSVTimeSeriesFile :

    def _init_(self,nome):
        self.nome = nome
        try :
             with open(self.nome ,'r') as file :
                 testo = file.read()
        except: 
            raise ExamException ('Il file non esiste oppure non e leggibile')
        
    def get_data(self):
        time_series =[]
        with open(self.nome ,'r') as file :
            for riga in file :
                elementi = riga.strip().split(',')
                if elementi[0] != 'dt' and len(elementi)== 2:
                    data = elementi[0]
                    try:
                        valore = float(elementi[1])
                        time_series.append([data,valore])
                    except:
                        print('errore il l elemento  non puo essere tipo float ')
                        continue
        return time_series           
    
def compute_variations (time_series,first_year,last_year,N):
    first_year = int(first_year)
    last_year = int(last_year)
    if N > len([first_year,last_year]):  
      raise ExamException('La lunghezza della finestra deve essere strettamente minore della dimensione dell intervallo')
    
    diz_anno_temperature = {}
    for lista in time_series :
        data = lista[0].strip()
        anno = data[:4]
        if anno >= first_year and anno <= last_year:
            if anno in diz_anno_temperature.keys():
                diz_anno_temperature[anno]=[]
            else:
                diz_anno_temperature[anno].append(lista[1])      
    diz_anno_media = {}    
    for anno in diz_anno_temperature.keys():
        somma = sum(diz_anno_temperature[anno])  
        lunghezza = len(diz_anno_temperature)
        if lunghezza > 0:
            media = somma/lunghezza
            diz_anno_media[anno]= media
    diz_variazioni={}   
    for anno in range(N+first_year,last_year+1) :
        media_anno=diz_anno_media(anno)
        media_anni_prec = 0
        for i in range(1,N+1):
            media_anni_prec+=diz_anno_media(anno-i)
        varianza = media_anno-media_anni_prec
        diz_variazioni[anno]=varianza
    return diz_variazioni    
if __name__=="main_":
    time_series_file =CSVTimeSeriesFile('GlobalTemperatures.csv')
    time_series= time_series_file.get_data()
    print(time_series)
    varianze=compute_variations(time_series,1900,1904,3)
    print(varianze)
