#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import sum
import os
from datetime import datetime
import glob


# In[2]:


def create_spark_session():
    """Crée une session Spark"""
    return SparkSession.builder \
        .appName("LogProcessing") \
        .getOrCreate()


# In[3]:


def get_hour_folders(base_path):
    """Récupère tous les dossiers horaires"""
    # Les dossiers sont au format YYYYMMDDHH
    return [d for d in os.listdir(base_path) if len(d) == 10 and d.isdigit()]


# In[4]:


def process_log_file(spark, file_path):
    """Traite un fichier log individuel"""
    try:
        # Lit le fichier avec Spark
        df = spark.read.option("delimiter", "|").csv(file_path)
        
        # Renomme les colonnes pour correspondre au format des logs
        df = df.toDF("timestamp", "id", "product_name", "currency", "price", "action")
        
        # Filtre les lignes avec action 'purchase' et convertit le prix en double
        df = df.filter(df.action == "purchase") \
              .withColumn("price", df.price.cast("double"))
        
        # Groupe par produit et somme les prix
        result_df = df.groupBy("product_name") \
                     .agg(sum("price").alias("total_price"))
        
        return result_df
    except Exception as e:
        print(f"Erreur lors du traitement du fichier {file_path}: {str(e)}")
        return None


# In[5]:


def format_datetime(folder_name):
    """Formate le nom du dossier en date lisible"""
    # Convertit YYYYMMDDHH en YYYY/MM/DD HH
    year = folder_name[:4]
    month = folder_name[4:6]
    day = folder_name[6:8]
    hour = folder_name[8:10]
    return f"{year}/{month}/{day} {hour}"


# In[6]:


def main():
    # Chemins
    input_path = "/home/jovyan/work/logs"
    output_path = "/home/jovyan/work/output"
    
    # Crée le dossier de sortie s'il n'existe pas
    os.makedirs(output_path, exist_ok=True)
    
    # Initialise Spark
    spark = create_spark_session()
    
    try:
        # Récupère tous les dossiers horaires
        hour_folders = get_hour_folders(input_path)
        
        for folder in hour_folders:
            folder_path = os.path.join(input_path, folder)
            
            # Récupère tous les fichiers logs dans le dossier (format: YYYYMMDDHHMMSS.txt)
            log_files = glob.glob(os.path.join(folder_path, "*.txt"))
            
            # Dictionnaire pour stocker les résultats de l'heure
            hour_results = {}
            
            # Traite chaque fichier de l'heure
            for file_path in log_files:
                result_df = process_log_file(spark, file_path)
                
                if result_df:
                    # Collecte les résultats
                    for row in result_df.collect():
                        product = row.product_name
                        amount = int(row.total_price * 100)  # Convertit en centimes
                        
                        if product not in hour_results:
                            hour_results[product] = 0
                        hour_results[product] += amount
            
            # Écrit les résultats dans un fichier pour cette heure
            if hour_results:
                output_file = os.path.join(output_path, f"{folder}.txt")
                date_str = format_datetime(folder)
                
                with open(output_file, 'a') as f:
                    for product, total in hour_results.items():
                        f.write(f"{date_str}|{product}|{total}\n")
                
                print(f"Fichier créé : {output_file}")
    
    finally:
        spark.stop()


# In[7]:


if __name__ == "__main__":
    # Décommentez la ligne suivante pour tester les formats
    # test_folders_and_files()
    main()


# In[ ]:




