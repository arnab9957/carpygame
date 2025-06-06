def show_settings_menu(self, background_surface):
    """Show the settings menu with proper fullscreen toggle"""
    # Create settings menu
    settings_menu = SettingsMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Main settings menu loop
    clock = pygame.time.Clock()
    while True:
        try:
            # Restore the background
            self.screen.blit(background_surface, (0, 0))

            # Draw and handle the settings menu
            settings_menu.draw()
            result = settings_menu.handle_input()

            if result == "BACK":
                # When returning from settings, make sure we have the correct screen
                self.screen = pygame.display.get_surface()
                return
            elif result == "EXIT":
                pygame.quit()
                sys.exit()
            elif result == "RESIZE" or result == "FULLSCREEN_CHANGED":
                # Update the stored background after resize or fullscreen change
                # Get the current screen surface which may have changed
                self.screen = pygame.display.get_surface()
                background_surface = self.screen.copy()
                
                # Update game dimensions
                global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
                SCREEN_WIDTH = self.screen.get_width()
                SCREEN_HEIGHT = self.screen.get_height()
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Recreate settings menu with new dimensions
                settings_menu = SettingsMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

            clock.tick(30)
        except Exception as e:
            print(f"Error in settings menu: {e}")
            traceback.print_exc()
            return
