import pygame
import numpy as np
import math
import sys
import time

def animar_maglev(x_vector, dt=0.05):
    """
    ANIMAR_MAGLEV - Anima el sistema de levitación magnética
    
    Inputs:
        x_vector - vector de posiciones de la pelota [cm] (desde techo hacia abajo)
        dt - tiempo entre frames [s] (opcional, default = 0.05s)
    
    Ejemplo:
        t = np.arange(0, 5, 0.1)
        x = 1 + 0.5*np.sin(2*np.pi*t)  # oscilación
        animar_maglev(x, 0.1)
    """
    
    # Parámetros del sistema (en cm)
    Tb = 1.4        # Ball travel (cm)
    db = 2.54       # Ball diameter (cm)
    rb = db/2       # Ball radius (cm)
    hp = 10         # Pedestal height (cm)
    techo_ancho = 8 # Ancho del electroimán
    techo_alto = 4  # Alto del electroimán
    pedestal_ancho = 3 # Ancho del pedestal
    
    # Configurar coordenadas del sistema
    y_pedestal_base = 0
    y_pedestal_top = hp
    y_pelota_min = y_pedestal_top + 2*rb
    y_pelota_max = y_pelota_min + Tb
    y_techo_base = y_pelota_max
    y_techo_top = y_techo_base + techo_alto
    y_origen = y_techo_base  # x=0 aquí
    
    # Configuración de pygame
    pygame.init()
    WIDTH = 600
    HEIGHT = 800
    SCALE = 30  # pixels por cm
    
    # Colores
    GRAY = (180, 180, 180)
    DARK_GRAY = (128, 128, 128)
    BLACK = (0, 0, 0)
    BLUE = (77, 77, 204)
    WHITE = (255, 255, 255)
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sistema Maglev')
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    
    def cm_to_pixels(x_cm, y_cm):
        """Convierte coordenadas de cm a pixels"""
        x_px = WIDTH//2 + x_cm * SCALE
        y_px = HEIGHT - (y_cm + 1) * SCALE  # +1 para margen inferior
        return int(x_px), int(y_px)
    
    def draw_system():
        """Dibuja los elementos fijos del sistema"""
        screen.fill(WHITE)
        
        # 1. DIBUJAR EL TECHO (ELECTROIMÁN)
        techo_points = [
            cm_to_pixels(-techo_ancho/2, y_techo_base),
            cm_to_pixels(techo_ancho/2, y_techo_base),
            cm_to_pixels(techo_ancho/2, y_techo_top),
            cm_to_pixels(-techo_ancho/2, y_techo_top)
        ]
        pygame.draw.polygon(screen, GRAY, techo_points)
        pygame.draw.polygon(screen, BLACK, techo_points, 2)
        
        # Rayas del electroimán
        for i in range(8):
            x_start = -techo_ancho/2 + i*techo_ancho/8
            x_end = x_start + techo_ancho/8
            start_pos = cm_to_pixels(x_start, y_techo_top)
            end_pos = cm_to_pixels(x_end, y_techo_base)
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)
        
        # 2. DIBUJAR EL PEDESTAL
        pedestal_points = [
            cm_to_pixels(-pedestal_ancho/2, y_pedestal_base),
            cm_to_pixels(pedestal_ancho/2, y_pedestal_base),
            cm_to_pixels(pedestal_ancho/2, y_pedestal_top),
            cm_to_pixels(-pedestal_ancho/2, y_pedestal_top)
        ]
        pygame.draw.polygon(screen, DARK_GRAY, pedestal_points)
        pygame.draw.polygon(screen, BLACK, pedestal_points, 2)
        
        # Grid simple
        for y in range(int(y_pedestal_base), int(y_techo_top) + 1, 2):
            start_pos = cm_to_pixels(-6, y)
            end_pos = cm_to_pixels(6, y)
            pygame.draw.line(screen, (230, 230, 230), start_pos, end_pos, 1)
    
    # 4. ANIMACIÓN
    running = True
    i = 0
    start_time = time.time()
    
    while running and i < len(x_vector):
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Verificar si es tiempo de actualizar
        if current_time - start_time >= dt:
            # Posición actual
            x = rb + x_vector[i]  # rb es offset mínimo
            
            # Convertir a coordenadas y
            y_pelota_centro = y_origen - x
            
            # Dibujar sistema fijo
            draw_system()
            
            # Dibujar pelota
            center_px = cm_to_pixels(0, y_pelota_centro)
            radius_px = int(rb * SCALE)
            pygame.draw.circle(screen, BLUE, center_px, radius_px)
            pygame.draw.circle(screen, BLACK, center_px, radius_px, 2)
            
            # Actualizar título
            title_text = f'Sistema Maglev - x={x-rb:.2f}cm (desde techo)'
            text_surface = font.render(title_text, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH//2, 30))
            screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            
            i += 1
            start_time = current_time
        
        clock.tick(60)  # Limitar FPS para suavidad
    
    # Mantener ventana abierta hasta que se cierre
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        clock.tick(60)
    
    pygame.quit()

# Ejemplo de uso
if __name__ == "__main__":
    # Crear vector de ejemplo (oscilación senoidal)
    t = np.arange(0, 5, 0.01)
    x = 0.7 + 0.5*np.sin(2*np.pi*t)  # oscilación de 1cm ± 0.5cm
    
    # Animar
    animar_maglev(x, 0.01)