Prehistorik 2 level format
==========================

By Jesses (mail at pre2 dot mine dot nu) and Dorten. \
Visit http://pre2.mine.nu for more Prehistorik 2 stuff

Level file format, v0.8.
Version history:
  0.8 - initial version

This file explains the format of LEVEL*.SQZ, after decompression.

# TLDR;
| BLock Name            | Start at / Offset | Bytes Size   |
| --------------------- | ----------------- | ------------ |
| Tile Map              | 0                 | 256 * height |
| Lookup Table          | 256 * height      | 512          |
| Tile Bitmaps          | 768               | 128 * max([lookup<256]) |
| Level infos:          | size(file) - 5029 | 5029         |
| - Tile Properties 1   |  -5029 + 0        |  256         |
| - Tile Properties 2   |  -5029 + 256      |  256         |
| - Tile Properties 3   |  -5029 + 512      |  256         |
| - Tile Properties 3   |  -5029 + 4031     |  256         |

### Bitmap Tiles 
Each tile is 16x16 pixels, 4bits per pixel = 128 bytes.

### Tiles Property 1
  `Horizontal properties`

  |  Value | Meaning |
  | :----: | ------- |
  |  1     | Solid sides |
  |  2     | Deadly from the sides |

### Tiles Property 2 
  `Vertical properties`
  |  Value | Meaning |
  | :----: | ------- |
  |  1     | Solid top, some of these tiles have different 'height', the player is forcing down through them a little (sample is bone rubbish at level E) |
  |  2     | Slightly slippery |
  |  3     | Slippery |
  |  4     | Not used in original levels, AFAIK, but if set makes floor VERY slippery (like in ttf) |
  |  5     | When standing on it and pressing down, becomes non-solid (hatches on level 2) |
  |  6     | Deadly from the top |

### Tiles Property 3 
  `Misc`
  |  Bit  |  Meaning |
  | :---: | ------- |
  |  0    |  Solid bottom |
  |  1    |  Deadly from the bottom |
  |  4    |  Seen only in combo with bit 6 on level 3. Flies are going out of it. |
  |  5    |  When stepped on, switches to next tile |
  |  6    |  Player is partially hidden behind the tile, see offset 777. |
  |  7    |  Tile is animated, using current and next two tiles (next two tiles are also animated, even if their third byte doesn't have bit 7 set) |

### Tiles Property 4
  `Slope information`
  |  Bit  |  Meaning |
  | :---: | ------- |
  |  0..3 |  Reversed height of left corner. Height of right corner depends on adjacent tile if not horizontal. |
  |  4    |  If set, tile is a slope going downright |
  |  5    |  If set, tile is a slope going upright |

    If bits 4..7 are 0, the tile is a horizontal floor.

## Level tiles height
All levels are 256 tiles wide, but their height varies. Unfortunately, you
need to know this height, but it's not stored in the file but in the
executable. Here is a table with the heights for each level:
```
1   2    3   4   5    6    7    8   9    A   B   C   D   E   F    G
49, 104, 49, 45, 128, 128, 128, 86, 110, 12, 24, 51, 51, 38, 173, 84
```

## Tilemap
The level file starts with a tile map, sized 256*height bytes. 
Each byte is actually an index in a lookup table of 256 16-bit values. 

## Lookup Table
This table is placed directly after the tilemap. 
The table contains 3 types of numbers:
less than 256, equal to 256 and greater than 256. 
* Tile 256 is transparent and shows the background picture. 
* Tiles 0..255 are level-specific tiles,
* while tiles 257+ are shared among the levels. 

## Small Number
You need to determine the maximum value among the level-specific tiles, so this 
maximum will be in the range 0..255; let's call this SmallNum. 
For these small numbers, a total of SmallNum 4-bit 16*16-sized tile bitmaps 
can be found directly after the lookup table (at byte offset number*128; 
`128` is the size in bytes one tile takes),
while for the larger numbers, the shared tiles are in the (compressed) file
UNION.SQZ at offset (number-256)*128.

An example to clarify: let's say we have a hypothetical level that's only one
tile high. Then at offset 0 in the level file, there's a 256*1 byte tilemap.
Let's say the first four bytes in the tilemap are 2, 1, 0, 3, and the rest of
the tilemap bytes are all 1.

# Lookup Table
After the tilemap, at offset 256, there is a lookup table sized 512 bytes.
Let's say the 16-bit values in this table at offsets `0, 1, 2, 3` are
respectively `270, 256, 214, 68`.
This means that the first(214) and fourth(68)
tile bitmaps are stored in the level file at offsets 256 x 1   + 512 + 214*128
and 256 x 1 + 512 + 68*128, 

| Offset | value | bitmap stored | offset   |
| ------ | ----- | ------------- | -------- |
|   0    |  214  | LEVEL*.SQZ    | 256x1 + 512 + 214 * 128 | 
|   1    |   68  | LEVEL*.SQZ    | 256x1 + 512 +  68 * 128 | 
|   2    |  256  |               |  -- TRANSPARENT --      | 
|   3    |  270  | UNION.SQZ     |     ( 270 - 256 ) * 128 | 

the third(270) tile bitmap is stored in UNION.SQZ at
offset 14*128 and the rest of the tiles are transparent (256), i.e. show the
background picture. 

Now SmallNum is the maximum of the values less than 256,
so the maximum of 214 and 68, which is 214. 

## Remaining data
The remainder of the level file is stored at offset 256x1 + 512 + 214*128.

This remaining part of the level file is not yet completely clear. It starts
at offset 256 x levelheight + 512 + SmallNum*128, or more conveniently put at
filesize - 5029. Let's call this position offset 0 from now on to keep things
simple.

Here's a table showing the remaining level structure, as far as it's known:

```
Offset  Size      What it is ("field: x" means that that field takes x bytes)

0       256       Tile properties byte 1
256     256       Tile properties byte 2
512     256       Tile properties byte 3
768     2         ????
770     2         X start
772     2         Y start
774     1         If tile with this x coord is the leftmost on screen, it
                  won't scroll right any further.
                  To get actual horizontal level size add 20.
775     1         ???? (in original levels always 0)
776     1         Scrolling behavior
777     256*2     For tile opacity: number of overlaying sprite for each tile.
1289    20*7      Gates:
                    xin: 1
                    yin: 1
                    xscreen: 1
                    yscreen: 1
                    xout: 1
                    yout: 1
                    scroll: 1
1429    15*10     Shifting tile blocks:
                    x: 1
                    y: 1
                    width: 1
                    height: 1
                    xact: 1
                    yact: 1
                    FFFF: 2 (constant)
                    dist: 1
                    00: 1 (constant)
1579    2048      Enemy records: (size of each record varies)
                    length: 1 (length of this record)
                    type/expert: 1
                    sprite: 2
                    unknown1: 1
                    hitpoints: 1
                    pause: 1
                    unknown2: 1
                    score: 1
                    x: 2
                    y: 2
                    type-specific: variable length (remainder of record)
3627    2         Item/platform sprite number offset
                  Actual_sprite_number = stored_sprite_number + 53 - offset
3629    2         Enemy sprite number offset
                  Actual_sprite_number = stored_sprite_number + 312 - offset
3631    80*5      Secrets:
                    FromTile: 1
                    ToTile: 1
                    Bonus/health: 1
                    x: 1
                    y: 1 
4031    256       Tile properties byte 4
4287    70*7      Items:
                    posx: 2
                    posy: 2
                    sprite: 2
                    00: 1 (constant)
4777    16*15     Platforms:
                    posx: 2
                    posy: 2
                    sprite: 2
                    behavior: 1
                    speed: 1
                    ????: 1 (always FF)
                    drop delay: 1
                    distance: 2
                    ????: 1 (always 0)
                    drop1?: 1
                    drop2?: 1
5017    2         Left border of Kong movement
5019    2         Right border of Kong movement
5021    1         ???? Kong-related, 2, 3 or -1. When set to 1, Kong starts
                  jumping on sight, when 5, he awakes only after a couple of
                  blows in the head. NOT sure about this one.
5022    2         Kong health
5024    1         ????  0 or -1 (if -1 => no Kong)
5025    2         Kong x coord
5027    2         Kong y coord
```

Now a detailed description for the above fields.


# Tile properties:
 offsets 0, 256, 512, 4031  \
  Four bytes per tile, in four 256-byte tables.

##  First byte (plain value) - Horizontal properties
    Value Meaning
    1     Solid sides
    2     Deadly from the sides

##  Second byte (plain value) - Vertical properties
    Value Meaning
    1     Solid top, some of these tiles have different 'height', the player
          is forcing down through them a little (sample is bone rubbish at
          level E)
    2     Slightly slippery
    3     Slippery
    4     Not used in original levels, AFAIK, but if set makes floor VERY
          slippery (like in ttf)
    5     When standing on it and pressing down, becomes non-solid
          (hatches on level 2)
    6     Deadly from the top

##  Third byte (bitfield) - misc
    Bit Meaning
    0   Solid bottom
    1   Deadly from the bottom
    4   Seen only in combo with bit 6 on level 3. Flies are going out of it.
    5   When stepped on, switches to next tile
    6   Player is partially hidden behind the tile, see offset 777.
    7   Tile is animated, using current and next two tiles (next two tiles are
        also animated, even if their third byte doesn't have bit 7 set)

##  Fourth byte (bitfield) - slope information
    Bit  Meaning
    0..3 Reversed height of left corner. Height of right corner depends on
         adjacent tile if not horizontal.
    4    If set, tile is a slope going downright
    5    If set, tile is a slope going upright

    If bits 4..7 are 0, the tile is a horizontal floor.

  About Partially transparent tiles: it must be a mask, because you can find
  both transparent and non-transparent pixels of the same color on one tile.
  Also, some tiles, like slopes on level 7 have variable height, but their
  properties are not different from simple ice...

## Unknown: offset 768

## Start: offset 770, 772
  Here you start the level.

## Scrolling limit: offset 774
  The screen won't scroll further to the right than this position, unless
  the player is to the right of it. In tiles, so multiply by 16 to get pixels.

## Unknown: offset 775

## Scrolling behavior: offset 776
  Bit Meaning
  0   Works with vertical scrolling. When not set, game tries to keep minimal
      distance between player and up/bottom of screen at about 2 tiles, when
      set, it's 4 tiles.
  1   When set, no horizontal scrolling. going to the right => death, more
      than 1 screen to left => also death
  2   When set, screen scrolls down by itself, going up => death

  So, in level 6 you get the value 6, but this behavior is forgotten as soon
  as the boss is awakened... If set to 0 or 1, the boss awakes at level start.
  This trick does not work with level 3's or level 9's bosses (i.e. the screen
  continues to descend)

## Opacity masks: offset 777
  When player/enemy goes near "masked" tile, the sprite from FRONT.SQZ with
  the corresponding number pops out and closes him.

## Gates: offset 1289
  In/out are the entrance/exit, screen is the screen's position after exiting
  the gate, scroll indicates whether the screen can scroll after going through.

## Shifting tile blocks: offset 1429
  No description yet.

## Enemies: offset 1579
  This one is a bit complicated: "length" is the number of bytes this enemy
  record contains; each enemy record is variable-length.
```
  Length:
    Length of record
  Type/expert:
    Bits 0..6 contain the enemy type. If bit 7 is set then this enemy is only
    present in expert mode.
  Sprite:
    Sprite number
  Unknown1:
    Not yet known, somehow affects behavior of type 9
    (0 - ignores gravity, 8 - not)
    type 2 spiders always have 1
    Type 0 have 3
    all others have 0
  Hitpoints:
    Enemy hitpoints (if not mistaken, throwing stoneaxe does 10 damage, club
    and hammer do damage, which depends on distance or even random
  Pause:
    Pause before activating actions in tenths of second (or something like
    that), for example a pause between jumps of jumping dino, or between death
    and spawn of type 0 and 10 enemies. Max value is 63. Anything more equals
    to eternity
  Unknown2:
    ????? seen only 00 or FF, maybe internally used
  Score:
    Score value: 0=>100, 1=>200 ... 11=>8000 (see sprite sequence)
  X, Y:
    Coordinate in pixels (if not type 0 or type 10)
  Type-specific:
    0: Falls from the sky, after landing walks, affected by gravity and walls.
       Active, when player is in The Area
      Length 13
      Bytes 9,10  - x,y coordinates of upper left corner of The Area
                    (instead of X, Y coordinates of the enemy)
      Bytes 11,12 - width and height of The Area
    1: Does not move, attack or die... Just a plain decoration (Spiderwebs)
      Length 13
    2: Moves up and down on a web (Spiders)
      Length 15
      Byte  13    - maximum web length
      Byte  14    - speed  
    3: Spawning spiders
      Length 14
      Byte  13    - Distance (in tiles?) at which it becames active.
    4: Pendulum spiders
      Length 17
      Byte  13    - Radius
      Byte  14    - Angle. Don't know in what units.
      Bytes 15,16 - always FF?
    5: Stands still, until player is on the line of sight, then moves
      diagonally down, when on the one horizontal with player - changes
      direction to horizontal (some bees at third and seventh levels)
      Length 16
      Byte  13    - width of rectangle, counted as line of sight (tiles)
      Byte  14    - height of rectangle, counted as line of sight (tiles)
      Byte  15    - Speed
    6: Clever flying enemy
      Length 21
      Byte  13    - distance of activating (horizontal) in tiles
      Other       - always FF?
    7: Stands still, until player is on the line of sight, then
       moves diagonally down
      Length 15
      Byte  13    - distance of activation (horizontal) in tiles
      Byte  14    - Speed
    8: Jumps (Dinos, leopards, little wormies...)
      Length 17
      Byte  13    - x  distance in tiles. When player is closer, starts
                    jumping (but waits some time at first, depending on its
                    'pause' value)
      Byte  14    - Vertical jump power. Height = VJP*(VJP+1)/2 pixels
      Byte  15    - Horizontal jump power.
      Byte  16    - like byte 13, but for vertical distance
    9: Goes left-right, ignoring walls (ignoring walls depends on byte 4
      (unknown1), in the case of penguins at level 7, can go by the slopes...
      But in other cases, not affected by gravity.)
      Length 19
      Bytes 13,14 - left border
      Bytes 15,16 - right border
      Byte  17    - always FF?
      Byte  18    - speed? (not clear, like with the next type)
    10: Spawns from the ground, walks some time, then goes underground again
      Length 14
      Bytes 9-12  - are used like in type 0
      Byte  13    - Not quite clear. Something like speed limit. (when set to
                    1, the enemy always stands still. Setting to 2 results in
                    sometimes_standing_but_sometimes_slowly_moving enemy, 
                    setting to 10 gives always_slowly_moving enemy, setting to
                    150 produces very_fast enemy. Needs further investigation)
    11: Flying squirrels. They can spawn at several different points, in a
      range of about 6 tiles (or maybe 100 pixels) up from x,y position
      Length 16
      Byte  13    - Horizontal speed
      Byte  14    - starting jump power (like in type 8)
      Byte  15    - Vertical speed
    12: Fast running penguins and cavemans 
      Seems, that they are activating, when x,y is about one screen away. Then
      they spawn at the edge of a screen. Nasty...
      Length 15
      Byte  13    - speed
      Byte  14    - always FF?
```
  Not sure about sprites. There may be hardcoded sprite sequences for 
  different enemy types. Setting sprite property to anything inappropriate 
  results in unpredictable behavior: when setting sprite of up-down moving 
  spider to 317 (spiderweb), there's a WASP, instead. When trying to create a
  jumping spider, there's jumping bears, transforming into leopards in the
  air, and SEVERE graphical artifacts (?!?). Setting the sprite of spawning
  spiders to 318 gives funny results :)
  Setting the sprite to an item sprite makes level not loadable.

## Sprite offsets: offsets 3627, 3629
  These need to be used to convert stored sprite numbers to actual sprite
  numbers.
  Actual_item_sprite_number = stored_item_sprite_number + 53 - item_offset
  Actual_enemy_sprite_number = stored_enemy_sprite_number + 312 - enemy_offset

## Secrets: offset 3631
  FromTile: Initial tile
  ToTile: Not used, tile changes to the tile on the map
          (in original levels tileTo=tile on the map, changing does no effect).
  Bonus/Health:
    00 to 3F: 1 to 64 small bonuses
    40 to 7F: 1 to 64 hits needed. Stars, dirt bits etc go out, depending on
              the level (maybe stored somewhere, maybe in exe, not yet known)
    80 to FF: Big bonus, hitpoints=(value-127)*x (or so) x is about 5 or 6
  If several such tiles are adjacent, they all change.
  If one of them changes and you hit several of them at one time, Bonus/Health
  of rightmost of the lowest row (from the ones you hit) is used (needs to be
  checked).

## Items: offset 4287
  Should also be clear. The level exit is also among the items.
  The last byte in the items records is always zero; if set to anything else,
  nothing changes ingame.

## Platforms: offset 4777
```
  Behavior:  
    Bit  Meaning
    0..2 Direction of moving
         7 0 1
         6 * 2
         5 4 3
         I.e. when 5, moves downwards towards the left.
    3    Dropdown
    7    If set, then platform works by itself; if not set, starts moving when
         player is on and stops at end of the cycle when he steps off
  Speed:
    Max speed of movement. If speed = zero and behavior = 08, then if stepped
    on platform drops down quickly until it hits solid ground (or into the
    abyss, if there is none) and waits, until player steps off
  Drop delay:
    If not dropdown - then FF
    If dropdown, the delay before dropping
  Distance:
    Time of moving on max speed if not dropdown, else zero
    Distance of moving: speed*(time+speed-1). Additional speed^2-speed is due
    to accelerating and braking.
  Drop1?:
    If not dropdown - zero, else = drop delay
  Drop2?:
    If not dropdown - zero, else = FF

Kong: offsets 5017, 5019, 5021, 5022, 5024, 5025, 5027
  Yeah, that's him: big dumb monkey. Tried to place him on 6th level. That was
  strange, you should try it yourself ;)
```

## Unknown entries among levels
Value of unknown entries in the original levels:

|  Level  |  768(int) |  775(byte) |
|  ------ | --------- | ---------- |
|    1    |     38    |     0     |
|    2    |     93    |     0     |
|    3    |     93    |     0     |
|    4    |     38    |     0     |
|    5    |     38    |     0     |
|    6    |    113    |     0     |
|    7    |    124    |     0     |
|    8    |     38    |     0     |
|    9    |      3    |     0     |
|    A    |    180    |     0     |
|    B    |     93    |     0     |
|    C    |     93    |     0     |
|    D    |     93    |     0     |
|    E    |      8    |     0     |
|    F    |      0    |     0     |
|    G    |    124    |     0     |

That's all for now... \
several bytes are still not clear. \
If you can tell me something about them, please do.
