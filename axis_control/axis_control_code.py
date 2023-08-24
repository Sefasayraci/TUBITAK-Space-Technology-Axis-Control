import serial
import time
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
import sys
import math


# Arduino ile seri iletişim kur
ser = serial.Serial('COM9', 9600)  # Port ve baud rate'i uygun şekilde ayarlayın

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

"""
# Uçak yüzey noktaları
vertices = np.array([
    [0, 0, 0],   # Burun
    [2, 0, 0],   # Sağ kanat ucu
    [-2, 0, 0],  # Sol kanat ucu
    [0, 0, -1],  # Kuyruk
    [0, 1, 0],   # Üst gövde
    [0, -1, 0],  # Alt gövde
])

# Yüzey üçgen indisleri
faces = np.array([
    [vertices[0], vertices[1], vertices[4]],
    [vertices[0], vertices[2], vertices[4]],
    [vertices[0], vertices[3], vertices[4]],
    [vertices[0], vertices[1], vertices[5]],
    [vertices[0], vertices[2], vertices[5]],
    [vertices[0], vertices[3], vertices[5]],
    [vertices[1], vertices[2], vertices[4]],
    [vertices[2], vertices[3], vertices[4]],
    [vertices[1], vertices[2], vertices[5]],
    [vertices[2], vertices[3], vertices[5]],
])

# Uçak yüzeylerini çiz
ax.add_collection3d(Poly3DCollection(faces, facecolors='blue', linewidths=1, edgecolors='black', alpha=0.6))

# Küp yüzey noktaları
vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

# Yüzey üçgen indisleri
faces = np.array([
    [vertices[0], vertices[1], vertices[5], vertices[4]],
    [vertices[7], vertices[6], vertices[2], vertices[3]],
    [vertices[0], vertices[4], vertices[7], vertices[3]],
    [vertices[1], vertices[5], vertices[6], vertices[2]],
    [vertices[0], vertices[1], vertices[2], vertices[3]],
    [vertices[4], vertices[5], vertices[6], vertices[7]],
])
"""

# Dikdörtgen yüzey noktaları
vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

# Dikdörtgen yüzey indisleri
faces = np.array([
    [vertices[0], vertices[1], vertices[2], vertices[3]],  # Alt yüzey
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # Üst yüzey
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # Ön yüzey
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Arka yüzey
    [vertices[0], vertices[3], vertices[7], vertices[4]],  # Sol yüzey
    [vertices[1], vertices[2], vertices[6], vertices[5]]   # Sağ yüzey
])

# Dikdörtgen yüzeylerini çiz
ax.add_collection3d(Poly3DCollection(faces, facecolors='black', linewidths=1, edgecolors='black', alpha=0.6, shade=False))


# Yüzeyleri farklı renklere boyamak için renkler
colors = ['black', 'black', 'black', 'black', 'black', 'black']

# Küp yüzeylerini çiz
ax.add_collection3d(Poly3DCollection(faces, facecolors=colors, linewidths=1, edgecolors='black', alpha=0.6))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Eksenlerin ölçeğini ayarla
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Küp dönüş açıları
roll = 0
pitch = 0

# Eksenleri kaldır
ax.set_axis_off()

# Ana döngü
# (Önceki kod bölümü burada yer alır...)

# Ana döngü

try:
    while not plt.waitforbuttonpress(timeout=0.01):  # Klavyeden bir tuşa basılıp basılmadığını kontrol et
        data = ser.readline().decode().strip()

        if data:
            roll, pitch = map(float, data.split('/'))
            ax.view_init(elev=pitch, azim=roll)
            
            # Küpün gidip gelme hareketini belirli bir aralıkla sağla
            max_translation = 1.5
            translation = max_translation * math.sin(time.time())
            ax.collections[1].set_verts([[v[0] + translation, v[1], v[2]] for v in vertices])
            
            plt.draw()
            plt.pause(0.01)

except KeyboardInterrupt:
    ser.close()
    print("Serial communication closed.")

plt.close()  # Pencereyi kapat
