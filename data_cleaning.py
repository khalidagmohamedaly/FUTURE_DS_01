"""
Data Cleaning Script for E-commerce Sales Data
Future Interns - Task 1: Business Sales Dashboard
Author: KHALID AG MOHAMED ALY
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data(filepath):
    """
    Charge les données depuis un fichier CSV
    """
    print("📂 Chargement des données...")
    df = pd.read_csv(filepath)
    print(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df

def clean_data(df):
    """
    Nettoie les données e-commerce
    """
    print("\n🧹 Nettoyage des données en cours...")
    
    # 1. Copie du dataframe
    df_clean = df.copy()
    
    # 2. Afficher les informations initiales
    print(f"\n📊 Aperçu initial:")
    print(df_clean.info())
    print(f"\n❌ Valeurs manquantes:\n{df_clean.isnull().sum()}")
    
    # 3. Supprimer les doublons
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    print(f"\n🗑️  {duplicates_removed} doublons supprimés")
    
    # 4. Gérer les valeurs manquantes
    # Supprimer les lignes avec des valeurs manquantes critiques
    critical_columns = ['Order ID', 'Product', 'Quantity', 'Price', 'Order Date']
    df_clean = df_clean.dropna(subset=critical_columns)
    
    # Remplir les valeurs manquantes non critiques
    if 'Customer ID' in df_clean.columns:
        df_clean['Customer ID'].fillna('Unknown', inplace=True)
    if 'Region' in df_clean.columns:
        df_clean['Region'].fillna('Unknown', inplace=True)
    
    print(f"✅ Valeurs manquantes traitées")
    
    # 5. Convertir les types de données
    if 'Order Date' in df_clean.columns:
        df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'], errors='coerce')
    
    # Assurer que Quantity et Price sont numériques
    df_clean['Quantity'] = pd.to_numeric(df_clean['Quantity'], errors='coerce')
    df_clean['Price'] = pd.to_numeric(df_clean['Price'], errors='coerce')
    
    # Supprimer les lignes avec des conversions échouées
    df_clean = df_clean.dropna(subset=['Quantity', 'Price', 'Order Date'])
    
    print(f"✅ Types de données convertis")
    
    # 6. Supprimer les valeurs aberrantes
    # Quantités et prix négatifs
    df_clean = df_clean[df_clean['Quantity'] > 0]
    df_clean = df_clean[df_clean['Price'] > 0]
    
    # Supprimer les valeurs extrêmes (au-delà de 3 écarts-types)
    for col in ['Quantity', 'Price']:
        mean = df_clean[col].mean()
        std = df_clean[col].std()
        df_clean = df_clean[
            (df_clean[col] >= mean - 3*std) & 
            (df_clean[col] <= mean + 3*std)
        ]
    
    print(f"✅ Valeurs aberrantes supprimées")
    
    # 7. Créer des colonnes dérivées
    df_clean['Total Sales'] = df_clean['Quantity'] * df_clean['Price']
    df_clean['Year'] = df_clean['Order Date'].dt.year
    df_clean['Month'] = df_clean['Order Date'].dt.month
    df_clean['Month Name'] = df_clean['Order Date'].dt.strftime('%B')
    df_clean['Quarter'] = df_clean['Order Date'].dt.quarter
    df_clean['Day of Week'] = df_clean['Order Date'].dt.day_name()
    
    print(f"✅ Colonnes dérivées créées")
    
    # 8. Standardiser les catégories
    if 'Category' in df_clean.columns:
        df_clean['Category'] = df_clean['Category'].str.strip().str.title()
    
    if 'Product' in df_clean.columns:
        df_clean['Product'] = df_clean['Product'].str.strip().str.title()
    
    if 'Region' in df_clean.columns:
        df_clean['Region'] = df_clean['Region'].str.strip().str.title()
    
    print(f"✅ Catégories standardisées")
    
    # 9. Résumé final
    print(f"\n✨ Nettoyage terminé!")
    print(f"📊 Données finales : {df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes")
    print(f"\n📅 Période des données : {df_clean['Order Date'].min()} à {df_clean['Order Date'].max()}")
    print(f"💰 Revenu total : ${df_clean['Total Sales'].sum():,.2f}")
    
    return df_clean

def generate_summary_stats(df):
    """
    Génère des statistiques descriptives
    """
    print("\n📈 STATISTIQUES DESCRIPTIVES")
    print("="*60)
    
    print("\n💰 Métriques Financières:")
    print(f"  - Revenu Total: ${df['Total Sales'].sum():,.2f}")
    print(f"  - Revenu Moyen par Commande: ${df['Total Sales'].mean():,.2f}")
    print(f"  - Prix Moyen: ${df['Price'].mean():,.2f}")
    
    print("\n📦 Métriques de Ventes:")
    print(f"  - Nombre Total de Commandes: {len(df):,}")
    print(f"  - Quantité Totale Vendue: {df['Quantity'].sum():,}")
    print(f"  - Quantité Moyenne par Commande: {df['Quantity'].mean():.2f}")
    
    if 'Category' in df.columns:
        print(f"\n🏷️  Catégories: {df['Category'].nunique()}")
        print(df['Category'].value_counts().head())
    
    if 'Product' in df.columns:
        print(f"\n📦 Produits Uniques: {df['Product'].nunique()}")
    
    if 'Region' in df.columns:
        print(f"\n🌍 Régions: {df['Region'].nunique()}")
        print(df['Region'].value_counts())
    
    return df.describe()

def save_cleaned_data(df, output_path):
    """
    Sauvegarde les données nettoyées
    """
    df.to_csv(output_path, index=False)
    print(f"\n💾 Données nettoyées sauvegardées : {output_path}")

def main():
    """
    Fonction principale
    """
    # Chemins des fichiers
    input_file = '../data/ecommerce_data.csv'
    output_file = '../data/data_cleaned.csv'
    
    try:
        # Charger les données
        df = load_data(input_file)
        
        # Nettoyer les données
        df_clean = clean_data(df)
        
        # Générer les statistiques
        stats = generate_summary_stats(df_clean)
        
        # Sauvegarder
        save_cleaned_data(df_clean, output_file)
        
        print("\n✅ PROCESSUS TERMINÉ AVEC SUCCÈS!")
        
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {input_file} n'a pas été trouvé.")
        print("💡 Astuce : Assurez-vous que le fichier est dans le dossier 'data/'")
    except Exception as e:
        print(f"❌ Erreur inattendue : {str(e)}")

if __name__ == "__main__":
    main()
