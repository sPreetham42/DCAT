import networkx as nx
import pandas as pd
import json

def build_joint_graph():
    print("Loading data...")
    # Load manifest for text groups
    manifest = pd.read_csv('experiments/75k_clean/ORIGINAL_PRE_REGISTERED_SPLIT/split_manifest.csv')
    manifest['email_id'] = manifest['email_id'].astype(str)
    
    # Load records to get labels and modalities
    df = pd.read_parquet('data/processed/records.parquet')
    df['email_id'] = df.index.astype(str)
    
    # Merge df with manifest to get text groups
    df = df.merge(manifest[['email_id', 'group_id']], on='email_id', how='inner')
    
    # Load image hashes
    img_hashes = pd.read_csv('scratch/image_hashes.csv')
    img_hashes['email_id'] = img_hashes['email_id'].astype(str)
    
    df = df.merge(img_hashes, on='email_id', how='left')
    
    print("Building joint graph...")
    G = nx.Graph()
    G.add_nodes_from(df['email_id'].tolist())
    
    # 1. Text edges (implicitly grouped by text group_id)
    # To avoid N^2 edges, we just use a star graph topology for each group to ensure connectivity
    grouped_text = df.groupby('group_id')['email_id'].apply(list)
    for group_emails in grouped_text:
        if len(group_emails) > 1:
            center = group_emails[0]
            edges = [(center, e) for e in group_emails[1:]]
            G.add_edges_from(edges)
            
    # 2. Image edges
    df_with_hashes = df.dropna(subset=['exact_hash'])
    grouped_imgs = df_with_hashes.groupby('exact_hash')['email_id'].apply(list)
    img_edges_added = 0
    for group_emails in grouped_imgs:
        if len(group_emails) > 1:
            center = group_emails[0]
            edges = [(center, e) for e in group_emails[1:]]
            G.add_edges_from(edges)
            img_edges_added += len(edges)
            
    print(f"Added {img_edges_added} explicit image-duplication edges.")
    
    print("Extracting connected components...")
    components = list(nx.connected_components(G))
    print(f"Total joint connected components: {len(components)}")
    
    # Map back to dataframe
    joint_group_map = {}
    for i, comp in enumerate(components):
        for e in comp:
            joint_group_map[e] = i
            
    df['joint_group_id'] = df['email_id'].map(joint_group_map)
    
    # Component statistics
    component_sizes = df['joint_group_id'].value_counts()
    singletons = len(component_sizes[component_sizes == 1])
    print(f"Singletons: {singletons}")
    print(f"Mean size: {component_sizes.mean():.2f}")
    print(f"Median size: {component_sizes.median():.2f}")
    print(f"95th percentile: {component_sizes.quantile(0.95):.2f}")
    print(f"Max size: {component_sizes.max()}")
    
    print("\nTop 20 Components:")
    print(component_sizes.head(20))
    
    gt_10 = component_sizes[component_sizes > 10].sum()
    gt_50 = component_sizes[component_sizes > 50].sum()
    gt_100 = component_sizes[component_sizes > 100].sum()
    print(f"\nRecords in components > 10: {gt_10}")
    print(f"Records in components > 50: {gt_50}")
    print(f"Records in components > 100: {gt_100}")
    
    # Effective Sample Size for image-bearing ham
    img_hams = df[(df['label'] == 0) & (df['has_meaningful_image'])]
    total_img_ham = len(img_hams)
    
    ham_group_counts = img_hams['joint_group_id'].value_counts()
    unique_groups = len(ham_group_counts)
    
    print(f"\nImage-bearing ham records: {total_img_ham}")
    print(f"Independent groups containing image-bearing ham: {unique_groups}")
    print("\nTop 5 ham groups by number of image-bearing hams:")
    
    cum_sum = 0
    for i, (gid, count) in enumerate(ham_group_counts.head(10).items()):
        total_size = component_sizes[gid]
        cum_sum += count
        if i in [0, 2, 4, 9]:
            print(f"Cumulative fraction in largest {i+1} components: {cum_sum / total_img_ham:.3f}")
        print(f"Joint Group {gid}: Total size = {total_size}, Image-Hams = {count}")
    
    # Save the dataframe with joint groups
    df.to_csv('scratch/joint_graph_df.csv', index=False)
    print("\nSaved joint graph data to scratch/joint_graph_df.csv")

if __name__ == "__main__":
    build_joint_graph()
