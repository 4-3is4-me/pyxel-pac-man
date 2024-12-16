## stuff to do..
## add more ghosts ; done
## add list for sprites ; done
## detect pac ghost collisions ; done
## add things to collect ; done
## control power pills, collection, timing, ghost behaviour; done
## game over and winning; done


# import the pyxel module
import pyxel
from objects.sprite import Sprite

# make a class for the App as they say in the instructions
class App:
    def __init__(self):

        #############################################################################################
        #                                                                                           #
        #                   INIT                                                                    #
        #                                                                                           #
        #############################################################################################

        # this is init which runs once at the start to set screen size, title, frame rate, etc
        pyxel.init(
            # width=160,
            # height=120,
            width=120,
            height=160,
            title="PAC-MAN",
            fps=30,
            quit_key=pyxel.KEY_X,
        )
        # load graphic and sound assets
        pyxel.load("sprite.pyxres")

        self.dummy_ghost = Sprite(
            name="dummy",
            image_bank=0,
            x=56,  # x=80,
            y=80,  # y=56,
            u=0,
            v=40,
            w=8,
            h=8,
            colkey=pyxel.COLOR_BLACK,
            speed=0,
        )

        # create a pacman object using my Sprite class
        self.pacman = Sprite(
            name="pacman",
            image_bank=0,
            x=56,  # x=76,
            y=112,  # y=72,
            u=0,
            v=0,
            w=8,
            h=8,
            colkey=pyxel.COLOR_BLACK,
            speed=2,  # having speed at 8 keeps Pac in line with tiles
        )

        # create a ghost object from the Sprite class
        self.blue_ghost = Sprite(
            name="blue",
            image_bank=0,
            x=56,  # x=64,
            y=79,  # y=55,
            u=0,
            v=8,
            w=8,
            h=8,
            colkey=pyxel.COLOR_BLACK,
            speed=1,
        )

        # create a ghost object from the Sprite class
        self.green_ghost = Sprite(
            name="green",
            image_bank=0,
            x=48,  # x=72,
            y=79,  # y=55,
            u=0,
            v=16,
            w=8,
            h=8,
            colkey=pyxel.COLOR_BLACK,
            speed=1,
        )

        self.red_ghost = Sprite(
            name="red",
            image_bank=0,
            x=56,  # x=80,
            y=64,  # y=55,
            u=0,
            v=24,
            w=8,
            h=8,
            colkey=pyxel.COLOR_BLACK,
            speed=1,
        )

        self.orange_ghost = Sprite(
            name="orange",
            image_bank=0,
            x=64,  # x=88,
            y=79,  # y=55,
            u=0,
            v=32,
            w=8,
            h=8,
            colkey=pyxel.COLOR_BLACK,
            speed=1,
        )

        # self.pacman.direction = "right"
        self.pill_count = 0
        self.small_pill = (2, 2)
        self.big_pill = (2, 3)
        self.blank_tile = (0, 5)
        self.start = True
        self.end = False
        self.score = 0

        # pyxel.sounds[0].set("e2e3e4", "p", "1", "n", 15)
        # pyxel.sounds[0].set("d-1rrrrrrrrr", "s", "1", "v", 15)
 

        for ghost in Sprite.sprite_list[2:]:
            ghost.target = Sprite.sprite_list[1]

        # pyxel.screen_mode(2) #classic, smooth, retro
        # pyxel.fullscreen(True)
        # display_scale=5,  # 10 = maximised window

        # run comes last in the App.init function to call update and draw functions
        pyxel.run(self.update, self.draw)

    ###########################################################################################
    #                                                                                         #
    #                   UPDATE                                                                #
    #                                                                                         #
    ###########################################################################################

    # ########### FUNCTIONS ########### #
    # timer
    def counting_down(self, sprite):
        if sprite.timer > 0:  #!= 0:
            sprite.timer -= 1
            return True
        else:
            return False

    def check_collisions(self):
        # pacman = Sprite.sprite_list[1]
        pacman_tile_location = (self.pacman.x // 8, self.pacman.y // 8)
        current_tile = pyxel.tilemaps[0].pget(
            pacman_tile_location[0],
            pacman_tile_location[1],
        )

        # if the tile at pacman location is the small pill
        if current_tile == self.small_pill:
            # count the number of small pills collected, break if all are collected
            if self.pill_count < 114:
                self.pill_count += 1
                self.score += 10
                # print(self.pill_count)
                # this changes the tile map at pacman location to a black tile to eat pills
                pyxel.tilemaps[0].pset(
                    pacman_tile_location[0],
                    pacman_tile_location[1],
                    self.blank_tile,
                )
            else:
                # print("you win")
                # clear the final pill
                pyxel.tilemaps[0].pset(
                    self.pacman.x // 8, self.pacman.y // 8, self.blank_tile
                )
                self.end = True

        # if the tile at pacman location is the big pill
        elif current_tile == self.big_pill:
            pyxel.tilemaps[0].pset(
                self.pacman.x // 8, self.pacman.y // 8, self.blank_tile
            )
            self.pacman.timer = 700
            for ghost in Sprite.sprite_list[2:]:
                # if ghost.u == 0:
                ghost.change_costume(1)
                ghost.timer = 60
                ghost.show = True
                ghost.target = Sprite.sprite_list[1]
                ghost.speed = 1


    # Pac controls, detect key press only when allowed to move, set direction
    def player_controls(self):
        # check if in line with tile
        if self.pacman.y % 8 == 0:
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                # check if light blue wall in the way
                if pyxel.pget(self.pacman.x + 9, self.pacman.y + 4) != 6:
                    self.pacman.direction = "right"
            elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                # check if light blue wall in the way
                if pyxel.pget(self.pacman.x - 2, self.pacman.y + 4) != 6:
                    self.pacman.direction = "left"

            # check if in line with tile
            if self.pacman.x % 8 == 0:
                if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                    # check if light blue wall in the way
                    if pyxel.pget(self.pacman.x + 4, self.pacman.y + 9) != 6:
                        self.pacman.direction = "down"
                elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                    # check if light blue wall in the way
                    if pyxel.pget(self.pacman.x + 4, self.pacman.y - 2) != 6:
                        self.pacman.direction = "up"


    def ghost_staus(self):
        for ghost in Sprite.sprite_list[2:]:
            catch = False

            if self.counting_down(self.pacman):
                pass
            else:
                if self.counting_down(ghost):
                    if pyxel.frame_count % 5 == 0:
                        if ghost.show:
                            ghost.show = False
                        else:
                            ghost.show = True
                        # if ghost.u == 8:
                        #    ghost.change_costume(3)
                        # else:
                        #    ghost.change_costume(1)
                else:
                    ghost.change_costume(0)
                    ghost.target = Sprite.sprite_list[1]
                    ghost.show = True

            # objective = ghost.target
            diff_x = ghost.x - ghost.target.x  # objective.x
            diff_y = ghost.y - ghost.target.y  # objective.y

            # #print(f"({diff_x},{diff_y})")
            if abs(diff_x) == 0 and abs(diff_y) < 10:
                catch = True
                # print("catch")
            elif abs(diff_x) < 10 and abs(diff_y) == 0:
                catch = True
                # print("catch")
            match ghost.u:
                # target is pacman
                case 0:
                    if catch:
                        # print("game over")
                        # exit()
                        self.end = True
                    else:
                        self.ghosts_direction(
                            ghost, diff_x, diff_y, "left", "right", "up", "down"
                        )
                        ghost.speed = 1
                # target is run away
                case 8:
                    if catch:
                        # print("dead ghost")
                        self.score += 50
                        ghost.change_costume(2)
                        ghost.target = Sprite.sprite_list[0]
                        # move to nearest block so speed 8 works
                        ghost.x = ghost.x - ghost.x % 8
                        ghost.y = ghost.y - ghost.y % 8
                        ghost.speed = 8
                    else:
                        self.ghosts_direction(
                            ghost, diff_x, diff_y, "right", "left", "down", "up"
                        )  ##
                # target is home
                case 16:
                    if catch:
                        ghost.change_costume(0)
                        ghost.target = Sprite.sprite_list[1]
                        ghost.timer = 0
                        ghost.speed = 1
                    else:
                        # print(f"{ghost.x},{ghost.y}")
                        tile = pyxel.tilemaps[1].pget(ghost.x // 8, ghost.y // 8)
                        match tile:
                            case (0, 6):
                                ghost.direction = "right"
                            case (1, 6):
                                ghost.direction = "left"
                            case (2, 6):
                                ghost.direction = "down"
                            case (3, 6):
                                ghost.direction = "up"
                            case _:
                                pass


    # picking the ghosts directions
    def ghosts_direction(self, ghost, diff_x, diff_y, dir_1, dir_2, dir_3, dir_4):
        directions = [dir_1, dir_2, dir_3, dir_4, dir_1, dir_2, dir_3, dir_4]
        random_direction = pyxel.rndi(0, 7)

        # some random to stop changing direction every frame???
        # if (pyxel.frame_count % 30) < rndi(1, 60):
        
        # if across is more than down
        if abs(diff_x) > abs(diff_y):
            # if diff_x is positive move ghost to the left
            if pyxel.sgn(diff_x) == 1:
                # check if in line with tile
                if ghost.y % 8 == 0:
                    # check if light blue wall in the way changed to <5 as no colours
                    # if the way is clear, go left
                    if pyxel.pget(ghost.x - 2, ghost.y + 4) < 5:  #!=6:
                        ghost.direction = dir_1
                    # else go in other rnd direction to help with getting stuck
                    else:
                        # print("RANDOM")
                        ghost.direction = directions[random_direction]
            # else diff_x is 0 or negative, move ghost to the right
            else:
                # check if in line with tile
                if ghost.y % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(ghost.x + 9, ghost.y + 4) < 5:  #!= 6:
                        ghost.direction = dir_2
                    else:
                        # print("RANDOM")
                        ghost.direction = directions[random_direction]
        # else down is more than across
        elif abs(diff_x) < abs(diff_y):
            # if diff_y is positve, move ghost up
            if pyxel.sgn(diff_y) == 1:
                # check if in line with tile
                if ghost.x % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(ghost.x + 4, ghost.y - 2) < 5:  #!= 6:
                        ghost.direction = dir_3
                    else:
                        # print("RANDOM")
                        ghost.direction = directions[random_direction]
            # else diff_y is 0 or negative, move ghost down
            else:
                # check if in line with tile
                if ghost.x % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(ghost.x + 4, ghost.y + 9) < 5:  #!= 6:
                        ghost.direction = dir_4
                    else:
                        # print("RANDOM")
                        ghost.direction = directions[random_direction]
        else:
            ghost.direction = directions[random_direction]
        # print(ghost.direction)

    def teleport(self, sprite):
        # dealing with the middle passages
        # for sprite in Sprite.sprite_list:
        if sprite.x < 0:
            sprite.x = pyxel.width
        if sprite.x > pyxel.width:
            sprite.x = 0
            
    # moving all the sprites when a direction has been set
    def move_sprite(self, sprite):
        match sprite.direction:
            case "right":
                # check if in line with tile
                if sprite.y % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(sprite.x + 9, sprite.y + 4) < 5:  #!= 6:
                        sprite.move(direction="right")
            case "left":
                # check if in line with tile
                if sprite.y % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(sprite.x - 2, sprite.y + 4) < 5:  #!= 6:
                        sprite.move(direction="left", flip_v=True)
            case "down":
                # check if in line with tile
                if sprite.x % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(sprite.x + 4, sprite.y + 9) < 5:  #!= 6:
                        if sprite.name == "pacman":
                            sprite.move(direction="down", rotation=270)
                        else:
                            sprite.move(direction="down")
            case "up":
                # check if in line with tile
                if sprite.x % 8 == 0:
                    # check if light blue wall in the way
                    if pyxel.pget(sprite.x + 4, sprite.y - 2) < 5:  #!= 6:
                        if sprite.name == "pacman":
                            sprite.move(direction="up", rotation=90)
                        else:
                            sprite.move(direction="up")
            case _:
                pass


    # ########### UPDATE ########## #
    # this is 'update' for events such as key presses and runs every frame
    
    def update(self):
        if self.start:
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.start = False
                # pyxel.play(0, 0, loop=True)
            # pass
        elif self.end:
            if pyxel.btn(pyxel.GAMEPAD1_BUTTON_X):
                quit()
            # pass
        else:
            pyxel.playm(0, loop=True)
            self.check_collisions()
            self.player_controls()
            self.ghost_staus()
            
            # move the ghosts up at the start
            if pyxel.frame_count < 30:
                self.red_ghost.direction = self.pacman.direction  # "right"
                self.green_ghost.direction = "up"
                self.blue_ghost.direction = "up"
                self.orange_ghost.direction = "up"

            for sprite in Sprite.sprite_list[1:]:
                self.teleport(sprite)
                self.move_sprite(sprite)

            # this bit makes pacman animate
            # make switch_costume and pass list of costumes to run though...??
            if pyxel.frame_count % 10 < 5:
                self.pacman.change_costume(1)
            else:
                self.pacman.change_costume(0)

    #########################################################################################
    #                                                                                       #
    #                   DRAW                                                                #
    #                                                                                       #
    #########################################################################################

    # ############ FUNCTIONS ########### #

    # draw the tile-map
    def draw_tilemap(self):
        pyxel.bltm(
            x=0,
            y=0,
            tm=0,
            u=0,
            v=0,
            w=pyxel.width,
            h=pyxel.height
        )

    # draw sprites if show is True
    def draw_sprites(self):
        for sprite in Sprite.sprite_list:
            if sprite.show:
                pyxel.blt(
                    x=sprite.x,
                    y=sprite.y,
                    img=sprite.image_bank,
                    u=sprite.u,
                    v=sprite.v,
                    w=sprite.w,
                    h=sprite.h,
                    colkey=sprite.colkey,
                    rotate=sprite.rotation,
                    scale=sprite.scale,
                )
    
    def draw_header(self, text):
        pyxel.text(
                    x=4,
                    y=2,
                    s=f"{text}",
                    col=pyxel.COLOR_WHITE
                )    

    def draw_score(self):
        pyxel.text(
                    x=72,
                    y=2,
                    s=f"SCORE: {self.score}",
                    col=pyxel.COLOR_WHITE
                )    

    # ############ DRAW ############# #
    # this is 'draw' for animations and moving things around on screen, runs when needed
    
    def draw(self):
        # clear the screen and fill with background colour-back_colour
        # pyxel.cls(pyxel.COLOR_BLACK)

        if self.start:
            self.draw_tilemap()
            self.draw_sprites()
            if pyxel.frame_count % 30 < 20:
                self.draw_header("PRESS LEFT OR RIGHT TO START")
        elif self.end:
            self.draw_tilemap()
            self.draw_sprites()
            if self.pill_count < 114:
                if pyxel.frame_count % 30 < 10:
                    self.pacman.show = False
                else:
                    self.pacman.show = True
                if pyxel.frame_count % 30 < 20:
                    self.draw_header("TOO BAD! HIT X")
                self.draw_score()
            else:
                self.draw_tilemap()
                self.draw_sprites()
                if pyxel.frame_count % 30 < 20:
                    self.draw_header("YOU WIN! HIT X")
                self.draw_score()

        else:
            self.draw_tilemap()
            self.draw_sprites()
            self.draw_header("PAC-MAN")
            self.draw_score()

# Start the App
App()

### NOTES

# setting the ghosts direction
# for ghost in Sprite.sprite_list[2:]:


# if self.pacman.power:
#    if self.power_timer == 0:
#        self.pacman.power = False
#        self.power_timer = 700
#        for ghost in Sprite.sprite_list[2:]:
#            ghost.change_costume(0)
#    else:
#        self.power_timer -= 1
# else:


# distance from pacman, calculating which is further, up or across
#        objective = Sprite.sprite_list[target]
#        diff_x = ghost.x - objective.x
#        diff_y = ghost.y - objective.y#
#
#        # #print(f"({diff_x},{diff_y})")
#        if abs(diff_x) == 0 and abs(diff_y) < 10:
#            #print("game over")
#            # quit()
#        elif abs(diff_x) < 10 and abs(diff_y) == 0:
#            #print("game over")
#            # quit()



# collision / location
# move ghosts
# directions = ["right", "left", "down", "up"]
#        if (pyxel.frame_count % 30) == 0:
# random_direction = rndi(0,3)
# self.blue_ghost.direction = directions[random_direction]
