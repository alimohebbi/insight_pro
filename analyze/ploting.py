import matplotlib.pyplot as plt
import numpy as np


def create_3d_plot2(topics):

    # Center coordinates of the sphere
    center_x = topics[0]['p']
    center_y = topics[1]['p']
    center_z = topics[2]['p']

    # Diameter of the sphere
    diameter = 0.01

    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create a meshgrid of points within the sphere's bounding box
    u = np.linspace(0, 2 * np.pi, 10)
    v = np.linspace(0, np.pi, 10)
    x = center_x + (diameter / 2) * np.outer(np.cos(u), np.sin(v))
    y = center_y + (diameter / 2) * np.outer(np.sin(u), np.sin(v))
    z = center_z + (diameter / 2) * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the sphere
    ax.plot_surface(x, y, z, color = 'g')

    # Set axis limits (adjust as needed)
    max_p = max(topics, key=lambda x: x['p'])['p']
    ax.set_xlim(0, max_p * 1.5)
    ax.set_ylim(0, max_p * 1.5)
    ax.set_zlim(0, max_p * 1.5)

    # Add labels for clarity (optional)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlabel(topics[0]['topic'])
    ax.set_ylabel(topics[1]['topic'])
    ax.set_zlabel(topics[2]['topic'])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.view_init(20, 65)
    plt.title('Company Important Dimensions')
    plt.show()


def create_3d_plot(topics):

    # Sample data (three lists representing x, y, and z values)
    x = [topics[0]['p']]
    y = [topics[1]['p']]
    z = [topics[2]['p']]
    max_p = max(topics, key=lambda x: x['p'])['p']
    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')
    # ax.contour3D(x, y, z, 50, cmap='binary')
    # Set axis labelsz


    ax.set_xlabel(topics[0]['topic'])
    ax.set_ylabel(topics[1]['topic'])
    ax.set_zlabel(topics[2]['topic'])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlim(0, 2*max_p)
    ax.set_ylim(0, 2*max_p)
    ax.set_zlim(0, 2*max_p)

    ax.view_init(20, 65)
    plt.show()
