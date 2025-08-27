import open3d as o3d
import os
import glob
import time
import natsort

def animate_pcd_sequence(directory):
    pcd_files = natsort.natsorted(glob.glob(os.path.join(directory, '*.pcd')))
    
    if not pcd_files:
        return

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    pcd = o3d.io.read_point_cloud(pcd_files[0])
    vis.add_geometry(pcd)

    viewer_control = vis.get_view_control()

    while True:
        for file_path in pcd_files:
            pcd_new = o3d.io.read_point_cloud(file_path)
            pcd.points = pcd_new.points
            if pcd_new.has_colors():
                pcd.colors = pcd_new.colors
            vis.update_geometry(pcd)
            vis.poll_events()
            vis.update_renderer()
            time.sleep(0.1)

    vis.destroy_window()

if __name__ == "__main__":
    pcd_directory = 'data/pcd/scene_2/'
    animate_pcd_sequence(pcd_directory)
