## stuff to do..
## add more ghosts ; done
## add list for sprites ; done
## detect pac ghost collisions ; done
## add things to collect ; done#
## control power pills, collection, timing, ghost behaviour; done
## game over and winning


# import the pyxel module, both ways to make pyxel.frame_count work and so to not have to
# type pyxel.xxxx for everything.
import pyxel
from pyxel import *
from objects.sprite import Sprite


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

# timer
def counting_down(sprite):
    if sprite.timer > 0: #!= 0:
        sprite.timer -= 1
        return True
    else:
        return False


# picking the ghosts directions
def ghosts_direction(ghost, diff_x, diff_y, dir_1, dir_2, dir_3, dir_4):
    directions = [dir_1, dir_2, dir_3, dir_4, dir_1, dir_2, dir_3, dir_4]
    random_direction = rndi(0, 7)

    # some random to stop changing direction every frame
    if (pyxel.frame_count % 30) < rndi(1, 60):
        # if across is more than down
        if abs(diff_x) > abs(diff_y):
            # if diff_x is positive move ghost to the left
            if sgn(diff_x) == 1:
                # check if in line with tile
                if ghost.y % 8 == 0:
                    # check if light blue wall in the way changed to <5 as no colours
                    ### if the way is clear, go left
                    if pget(ghost.x - 2, ghost.y + 4) < 5:  #!=6:
                        ghost.direction = dir_1
                    # else go in other rnd direction to help with getting stuck
                    else:
                        #print("RANDOM")
                        ghost.direction = directions[random_direction]
            # else diff_x is 0 or negative, move ghost to the right
            else:
                # check if in line with tile
                if ghost.y % 8 == 0:
                    # check if light blue wall in the way
                    if pget(ghost.x + 9, ghost.y + 4) < 5:  #!= 6:
                        ghost.direction = dir_2
                    else:
                        #print("RANDOM")
                        ghost.direction = directions[random_direction]
        # else down is more than across
        elif abs(diff_x) < abs(diff_y):
            # if diff_y is positve, move ghost up
            if sgn(diff_y) == 1:
                # check if in line with tile
                if ghost.x % 8 == 0:
                    # check if light blue wall in the way
                    if pget(ghost.x + 4, ghost.y - 2) < 5:  #!= 6:
                        ghost.direction = dir_3
                    else:
                        #print("RANDOM")
                        ghost.direction = directions[random_direction]
            # else diff_y is 0 or negative, move ghost down
            else:
                # check if in line with tile
                if ghost.x % 8 == 0:
                    # check if light blue wall in the way
                    if pget(ghost.x + 4, ghost.y + 9) < 5:  #!= 6:
                        ghost.direction = dir_4
                    else:
                        #print("RANDOM")
                        ghost.direction = directions[random_direction]
        else:
            ghost.direction = directions[random_direction]
        #print(ghost.direction)


# moving all the sprites when a direction has been set
def move_sprite(sprite):

    # dealing with the middle passages
    # for sprite in Sprite.sprite_list:
    if sprite.x < 0:
        sprite.x = 158
    if sprite.x > 159:
        sprite.x = 0

    match sprite.direction:
        case "right":
            # check if in line with tile
            if sprite.y % 8 == 0:
                # check if light blue wall in the way
                if pget(sprite.x + 9, sprite.y + 4) < 5:  #!= 6:
                    sprite.move(direction="right")
        case "left":
            # check if in line with tile
            if sprite.y % 8 == 0:
                # check if light blue wall in the way
                if pget(sprite.x - 2, sprite.y + 4) < 5:  #!= 6:
                    sprite.move(direction="left", flip_v=True)
        case "down":
            # check if in line with tile
            if sprite.x % 8 == 0:
                # check if light blue wall in the way
                if pget(sprite.x + 4, sprite.y + 9) < 5:  #!= 6:
                    if sprite.name == "pacman":
                        sprite.move(direction="down", rotation=270)
                    else:
                        sprite.move(direction="down")
        case "up":
            # check if in line with tile
            if sprite.x % 8 == 0:
                # check if light blue wall in the way
                if pget(sprite.x + 4, sprite.y - 2) < 5:  #!= 6:
                    if sprite.name == "pacman":
                        sprite.move(direction="up", rotation=90)
                    else:
                        sprite.move(direction="up")
        case _:
            pass
    ##print(f"{sprite.name}, {sprite.direction}")


# make a class for the App as they say in the instructions
class App:
    def __init__(self):

        #############################################################################################
        #                                                                                           #
        #                   INIT()                                                                  #
        #                                                                                           #
        #############################################################################################

        # this is init which runs once at the start to set screen size, title, frame rate, etc
        init(
            width=160,
            height=120,
            title="PAC-MAN",
            fps=30,
            quit_key=KEY_Q,
            # display_scale=10,  # maximised window?
        )
        # load graphic and sound assets
        load("sprite.pyxres")

        self.dummy_ghost = Sprite(
            name="dummy",
            image_bank=0,
            x=80,
            y=56,
            u=0,
            v=40,
            w=8,
            h=8,
            colkey=COLOR_BLACK,
            speed=0,
        )

        # create a pacman object using my Sprite class
        self.pacman = Sprite(
            name="pacman",
            image_bank=0,
            x=76,
            y=72,
            u=0,
            v=0,
            w=8,
            h=8,
            colkey=COLOR_BLACK,
            speed=2,  # having speed at 8 keeps Pac in line with tiles
        )

        # create a ghost object from the Sprite class
        self.blue_ghost = Sprite(
            name="blue",
            image_bank=0,
            x=64,
            y=55,
            u=0,
            v=8,
            w=8,
            h=8,
            colkey=COLOR_BLACK,
            speed=1,
        )

        # create a ghost object from the Sprite class
        self.green_ghost = Sprite(
            name="green",
            image_bank=0,
            x=72,
            y=55,
            u=0,
            v=16,
            w=8,
            h=8,
            colkey=COLOR_BLACK,
            speed=1,
        )

        self.red_ghost = Sprite(
            name="red",
            image_bank=0,
            x=80,
            y=55,
            u=0,
            v=24,
            w=8,
            h=8,
            colkey=COLOR_BLACK,
            speed=1,
        )

        self.orange_ghost = Sprite(
            name="orange",
            image_bank=0,
            x=88,
            y=55,
            u=0,
            v=32,
            w=8,
            h=8,
            colkey=COLOR_BLACK,
            speed=1,
        )

        self.pacman.direction = "right"
        self.pill_count = 0
        self.small_pill = (2, 2)
        self.big_pill = (2, 3)
        self.blank_tile = (0, 5)

        for ghost in Sprite.sprite_list[2:]:
            ghost.target = Sprite.sprite_list[1]

        # pyxel.screen_mode(2) #classic, smooth, retro
        # pyxel.fullscreen(True)

        # run comes last in the App.init function to call update and draw functions
        run(self.update, self.draw)

    ###########################################################################################
    #                                                                                         #
    #                   UPDATE()                                                              #
    #                                                                                         #
    ###########################################################################################

    # this is 'update' for events such as key presses and runs every frame
    def update(self):

        # collision / location
        # move ghosts
        # directions = ["right", "left", "down", "up"]
        #        if (pyxel.frame_count % 30) == 0:

        # #print(f"{diff_x},{diff_y}")
        # random_direction = rndi(0,3)
        # self.blue_ghost.direction = directions[random_direction]
        # move these as constant?
        # if self.pacman.x < 0:
        #    self.pacman.x = 158
        # if self.pacman.x > 159:
        #    self.pacman.x = 0

        pacman = Sprite.sprite_list[1]

        current_tile = pyxel.tilemaps[0].pget(
            (self.pacman.x // 8), (self.pacman.y // 8)
        )

        # if the tile at pacman location is the small pill
        if current_tile == self.small_pill:
            # count the number of small pills collected, break if all are collected
            if self.pill_count < 127:
                self.pill_count += 1
                # #print(self.pill_count)  # 132
                # this changes the tile map at pacman location to a black tile to eat pills
                pyxel.tilemaps[0].pset(
                    self.pacman.x // 8, self.pacman.y // 8, self.blank_tile
                )
            else:
                print("you win")
                # clear the final pill
                pyxel.tilemaps[0].pset(
                    self.pacman.x // 8, self.pacman.y // 8, self.blank_tile
                )
                # do more...

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
            
            

        # Pac controls, detect key press only when allowed to move, set direction
        # check if in line with tile
        if self.pacman.y % 8 == 0:
            if btn(KEY_RIGHT):
                # check if light blue wall in the way
                if pget(self.pacman.x + 9, self.pacman.y + 4) != 6:
                    self.pacman.direction = "right"
            elif btn(KEY_LEFT):
                # check if light blue wall in the way
                if pget(self.pacman.x - 2, self.pacman.y + 4) != 6:
                    self.pacman.direction = "left"

            # check if in line with tile
            if self.pacman.x % 8 == 0:
                if btn(KEY_DOWN):
                    # check if light blue wall in the way
                    if pget(self.pacman.x + 4, self.pacman.y + 9) != 6:
                        self.pacman.direction = "down"
                elif btn(KEY_UP):
                    # check if light blue wall in the way
                    if pget(self.pacman.x + 4, self.pacman.y - 2) != 6:
                        self.pacman.direction = "up"

        # setting ghost directions
        for ghost in Sprite.sprite_list[2:]:
            catch = False

            if counting_down(self.pacman):
                pass
            else:
                if counting_down(ghost):
                    if pyxel.frame_count % 5 == 0:
                        if ghost.show:
                            ghost.show = False
                        else:
                            ghost.show = True
                        #if ghost.u == 8:
                        #    ghost.change_costume(3)
                        #else:
                        #    ghost.change_costume(1)
                else:
                    ghost.change_costume(0)
                    ghost.target = Sprite.sprite_list[1]
                    ghost.show = True
                    

            #objective = ghost.target
            diff_x = ghost.x - ghost.target.x #objective.x
            diff_y = ghost.y - ghost.target.y #objective.y

            # #print(f"({diff_x},{diff_y})")
            if abs(diff_x) == 0 and abs(diff_y) < 10:
                catch = True
                print("catch")
            elif abs(diff_x) < 10 and abs(diff_y) == 0:
                catch = True
                print("catch")
            match ghost.u:
                # target is pacman
                case 0:
                    if catch:
                        print("game over")
                        exit()
                    else:
                        ghosts_direction(
                            ghost, diff_x, diff_y, "left", "right", "up", "down"
                        )
                # target is run away
                case 8:
                    if catch:
                        #print("dead ghost")
                        ghost.change_costume(2)
                        ghost.target = Sprite.sprite_list[0]
                        #ghost.speed = 2
                    else:
                        ghosts_direction(
                            ghost, diff_x, diff_y, "right", "left", "down", "up"
                        )  ##
                # target is home
                case 16:
                    if catch:
                        ghost.change_costume(0)
                        ghost.target = Sprite.sprite_list[1]
                        ghost.direction = "up" ##notcertain
                        ghost.timer = 0
                        #ghost.speed = 1
                    else:
                        ##print(f"{ghost.x},{ghost.y}")
                        # hard coded to get dead ghosts home... they get stuck in other places too..
                        if ghost.y == 72:
                            if ghost.x > 54 and ghost.x < 100:
                                ghost.direction = "right"
                                ##print("RIGHT")
                            else:
                                if ghost.x > 99 and ghost.x < 105:
                                    #if counting_down(ghost):
                                    ghost.direction = "up"
                                    #else:
                                    #    ghost.timer = 120
                                    ##print("UP")
                                else:
                                    ##print("ELSE1")
                                    ghosts_direction(
                                        ghost,
                                        diff_x,
                                        diff_y,
                                        "left",
                                        "right",
                                        "up",
                                        "down",
                                    )

                        else:
                            # #print(f"{ghost.x},{ghost.y}")
                            ##print("ELSE")
                            ghosts_direction(
                                ghost, diff_x, diff_y, "left", "right", "up", "down"
                            )

        # move the ghosts up at the start
        if pyxel.frame_count < 30:
            self.red_ghost.direction = "up"
            self.green_ghost.direction = "up"

        for sprite in Sprite.sprite_list[1:]:
            move_sprite(sprite)

        # this bit makes pacman animate
        # make switch_costume and pass list of costumes to run though...??
        if pyxel.frame_count % 10 < 5:
            self.pacman.change_costume(1)
        else:
            self.pacman.change_costume(0)

    #########################################################################################
    #                                                                                       #
    #                   DRAW()                                                              #
    #                                                                                       #
    #########################################################################################

    #    # this is 'draw' for animations and moving things around on screen, runs when needed
    def draw(self):

        back_colour = COLOR_BLACK  # 0-15
        text_x = 50
        text_y = 66
        text_colour = COLOR_GREEN  # 0-15

        # clear the screen and fill with background colour-back_colour
        # cls(back_colour)

        # draw the tile-map
        bltm(0, 0, 0, 0, 0, 160, 120)

        # write text in the location x,y
        # if pyxel.frame_count < 30:
        #     text(text_x, text_y, f"GO GO GO!", text_colour)

        # if ((pyxel.frame_count % 30 < 15) == 0):

        # draw pacman if show is True
        #        if self.pacman.show:
        #            blt(
        #                self.pacman.x,
        #                self.pacman.y,
        #                self.pacman.image_bank,
        #                self.pacman.u,
        #                self.pacman.v,
        #                self.pacman.w,
        #                self.pacman.h,
        #                self.pacman.colkey,
        #                rotate=self.pacman.rotation,
        #                scale=self.pacman.scale,
        #            )

        # draw ghost if show is True
        #        if self.blue_ghost.show:
        #            blt(
        #                self.blue_ghost.x,
        #                self.blue_ghost.y,
        #                self.blue_ghost.image_bank,
        #                self.blue_ghost.u,
        #                self.blue_ghost.v,
        #                self.blue_ghost.w,
        #                self.blue_ghost.h,
        #                self.blue_ghost.colkey,
        #                rotate=self.blue_ghost.rotation,
        #                scale=self.blue_ghost.scale,
        #            )
        for sprite in Sprite.sprite_list:
            # draw ghost if show is True
            if sprite.show:
                blt(
                    sprite.x,
                    sprite.y,
                    sprite.image_bank,
                    sprite.u,
                    sprite.v,
                    sprite.w,
                    sprite.h,
                    sprite.colkey,
                    rotate=sprite.rotation,
                    scale=sprite.scale,
                )

# Start the App
App()
