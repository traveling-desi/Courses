;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Searching for optimum solution to Kauffman's
;; NK Fitness landscapes by agents situated on a small world topology
;; written by Lada Adamic and heavily borrowing from
;; HeuristicSearch_KauffmanNK1.nlogo by
;; Christopher J Watts, 2011
;; Based on:
;; Kauffman, S (1993) "The Origins of Order"
;; Kauffman, S (1995) "At Home in the Universe"
;; Kauffman, S (2000) "Investigations"
;; D Lazer and A. Friedman (2007) "The Network Structure of Exploration and Exploitation"
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


extensions [array]

globals [
  mean-fitness
  max-fitness
  initial-mean-fitness
  initial-max-fitness
  
  input-sets
  fitness-tables
  
  new-node
  
  output-every
  
  probabilities
  degrees
  
  x
]

turtles-own [
  fitness
  solution
  alt-solution
  alt-fitness
  
  initial-solution
  initial-fitness
]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to setup
  ;; (for this model to work with NetLogo's new plotting features,
  ;; __clear-all-and-reset-ticks should be replaced with clear-all at
  ;; the beginning of your setup procedure and reset-ticks at the end
  ;; of the procedure.)
  __clear-all-and-reset-ticks
  
  setup-nk
  
  set output-every 100
  set probabilities array:from-list n-values n-nodes [0.5]
  
  create-turtles number-of-turtles [
    set size 2
    set shape "circle"
    
    set solution array:from-list (map [ifelse-value (? > random-float 1) [1] [0] ] (array:to-list probabilities))
    calc-turtle-fitness
    set x solution
;    let rcolor get-color
    set color get-color  
 ;   set color ( list (255 - fitness * 255) 0 (fitness * 255))

    
    set initial-solution array:from-list array:to-list solution
    set initial-fitness fitness
  ]
  
  set mean-fitness mean [fitness] of turtles
  set max-fitness max [fitness] of turtles
  set initial-mean-fitness mean-fitness
  set initial-max-fitness max-fitness
  
  my-setup-plots
  
  ;; Layout turtles:
  layout-circle (sort turtles) max-pxcor - 8
  
  create-small-world
  
end


to reset-turtles
  ; Without defining the NK fitness landscape, set turtle population back to their intial starting points.
  clear-all-plots
  ask turtles [
    set solution array:from-list array:to-list initial-solution
    set fitness initial-fitness
  ]
  set mean-fitness mean [fitness] of turtles
  set max-fitness max [fitness] of turtles
  set probabilities array:from-list n-values n-nodes [0.5]
  
  my-setup-plots
  
end  

;; create small world topology
to create-small-world
  ;; iterate over the nodes
  
  ; create regular lattice with links to 2 closests neighbors
  let n 0
  while [n < count turtles]
  [
    ;; connect to closest neighbor
    ask turtle n [
              create-link-with
              turtle ((n + 1) mod count turtles)
    ]
    set n n + 1
  ]
  
  repeat num-additional [ 
    ask one-of turtles [
      if any? other turtles with [(not link-neighbor? self)][
          create-link-with one-of other turtles with [not link-neighbor? self ]
      ]
    ]
  ]
end
 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to setup-NK
  ; Define input nodes for each node
  set input-sets array:from-list n-values n-nodes [array:from-list n-values (k-inputs + 1) [random (n-nodes - 1)]]
  let cur-node 0
  let cur-input 0
  let input-set array:from-list n-values (k-inputs + 1) [0]
  repeat n-nodes [
    set input-set array:item input-sets cur-node
    set cur-input 0
    array:set input-set 0 cur-node ; Each node is an input to itself
    repeat k-inputs [ ; Each node has K inputs which are not itself
      set cur-input cur-input + 1
      if (array:item input-set cur-input) >= cur-node [array:set input-set cur-input ((array:item input-set cur-input) + 1)]
    ]
    set cur-node cur-node + 1
  ]
  
  ; Define fitness table for each node
  set fitness-tables array:from-list n-values n-nodes [array:from-list n-values (2 ^ (k-inputs + 1)) [random-float 1]]
end

to calc-turtle-fitness
  let fitness-sum 0
  let cur-node 0
  repeat n-nodes [
    set fitness-sum fitness-sum + 
      array:item (array:item fitness-tables cur-node) (sum n-values (k-inputs + 1) [(array:item solution (array:item (array:item input-sets cur-node) ?)) * (2 ^ ?)])
    
    set cur-node cur-node + 1
  ]
  
  set fitness (fitness-sum / n-nodes)
  ;set fitness ((fitness-sum / n-nodes) / base-max-fitness) ^ 8 ; Lazer & Friedman's definition
  
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to go
  if (ticks > max-iterations) [stop]
  copy-or-innovate
  
  set mean-fitness mean [fitness] of turtles
  set max-fitness max [fitness] of turtles
  
  tick

  if (ticks mod output-every) = 0 [my-update-plots]
  
end

to copy-or-innovate

  ask one-of turtles [
    set size 4
    let my-own-fitness fitness
    let best-fitness fitness
    let best-solution solution
    ask link-neighbors [
      set size 4
      if (fitness > best-fitness) [
        set best-fitness fitness
        set best-solution solution
      ]
      set size 2
    ]
    
    ifelse (my-own-fitness = best-fitness) [
      set alt-fitness fitness
      let cur-node (random n-nodes)
      let alt-state array:item solution cur-node
      array:set solution cur-node (1 - alt-state)
      calc-turtle-fitness
      if fitness < alt-fitness [
        ; roll back
        array:set solution cur-node alt-state
        set fitness alt-fitness
      ]
    ][
      set solution best-solution
      calc-turtle-fitness
    ]    
 
    set x solution
    set color get-color   

    set size 2
  ]

end

to-report get-color

  let red-color 0
  let green-color 0
  let blue-color 0
  
  let i 0
  while [i < 8] [
    set red-color (red-color + (array:item x i) * 2 ^ i)
    set i (i + 1)
    ]
  
  while [i < 16] [
    set green-color (green-color + (array:item x i) * 2 ^ (i - 8))
    set i (i + 1)
    ]
    
   while [i < 24] [
    set blue-color (blue-color + (array:item x i) * 2 ^ (i - 16))
    set i (i + 1)
    ]
  
  report (list red-color green-color blue-color)
end

to generate-ba-topology
  ;; (for this model to work with NetLogo's new plotting features,
  ;; __clear-all-and-reset-ticks should be replaced with clear-all at
  ;; the beginning of your setup procedure and reset-ticks at the end
  ;; of the procedure.)
  ca
  
  reset-ticks
  setup-nk
  
  set output-every 100
  set probabilities array:from-list n-values n-nodes [0.5]
  
  set-default-shape turtles "circle"
  set degrees []   ;; initialize the array to be empty
  ;; make the initial network of two turtles and an edge
  
  make-node ;; add the very first node
  
  let first-node new-node  ;; remember that its the first node
  
  ;; the following few lines create a cycle of length 5
  ;; this is just an arbitrary way to start a network
  
  let prev-node new-node
  repeat 4 [
    make-node ;; second node
    make-edge new-node prev-node ;; make the edge
    set degrees lput prev-node degrees
    set degrees lput new-node degrees
    set prev-node new-node
  ]
  make-edge new-node first-node

  while [count turtles < number-of-turtles] [
    ;; new edge is green, old edges are gray
    ask links [ set color gray + 2]
    ;; old turtles are blue
    ask turtles [set color gray + 2]
  
    make-node  ;; add one new node
  
    let partner find-partner new-node      ;; find a partner for the new node
    ask partner [set color gray + 2]    ;; set color of partner to gray
    make-edge new-node partner     ;; connect it to the partner we picked before
    
    do-layout
  ]

  ask turtles [
        set solution array:from-list (map [ifelse-value (? > random-float 1) [1] [0] ] (array:to-list probabilities))
    calc-turtle-fitness
    set x solution
;    let rcolor get-color
    set color get-color  
 ;   set color ( list (255 - fitness * 255) 0 (fitness * 255))

    
    set initial-solution array:from-list array:to-list solution
    set initial-fitness fitness
  ]
  
  set mean-fitness mean [fitness] of turtles
  set max-fitness max [fitness] of turtles
  set initial-mean-fitness mean-fitness
  set initial-max-fitness max-fitness

end

;; connects the two turtles
to make-edge [node1 node2]
  ask node1 [
    ifelse (node1 = node2) 
    [
      show "error: self-loop attempted"
    ]
    [
      create-link-with node2 [ set color green ]
     ;; position the new node near its partner
      setxy ([xcor] of node2) ([ycor] of node2)
      rt random 360
      fd 8
      set degrees lput node1 degrees
     set degrees lput node2 degrees
     ]
  ]
end

to make-node
  create-turtles 1  ;; don't know what this is - lada
  [
    set color gray + 2
    set size 2
    set new-node self ;; set the new-node global
  ]
end

to-report find-partner [node1]
  ;; set a local variable called ispref that
  ;; determines if this link is going to be
  ;; preferential of not
  let ispref (random-float 1 <= prob-pref)
  
  ;; initialize partner to be the node itself
  ;; this will have to be changed
  let partner node1
  
  ;; if preferential attachment then choose
  ;; from our degrees array
  ;; otherwise chose one of the turtles at random
  ifelse ispref 
  [
    set partner one-of degrees
   ]
   [
     set partner one-of turtles
     ]
     
   ;; but need to check that partner chosen isn't
   ;; the node itself and also isn't a node that
   ;; our node is already connected to
   ;; if this is the case, it will try another
   ;; partner and try again
  let checkit true
  while [checkit] [
    ask partner [
      ifelse ((link-neighbor? node1) or (partner = node1))
        [
          ifelse ispref 
          [
            set partner one-of degrees
           ]
           [
             set partner one-of turtles
           ]
            set checkit true
         ]
         [
           set checkit false
         ]
       ] 
    ]
  report partner
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
to my-setup-plots
  set-current-plot "Fitness"
  set-current-plot-pen "Mean"
  set-plot-pen-interval output-every
  set-current-plot-pen "Max"
  set-plot-pen-interval output-every
  
  set-current-plot "Fitness-Histogram"
  set-plot-pen-interval 0.05
  histogram [fitness] of turtles
end

to my-update-plots
  set-current-plot "Fitness"
  set-current-plot-pen "Mean"
  plot mean-fitness
  set-current-plot-pen "Max"
  plot max-fitness
  
  set-current-plot "Fitness-Histogram"
  set-plot-pen-interval 0.05
  histogram [fitness] of turtles
end

;;layout all nodes and links
to do-layout
  repeat 5 [layout-spring turtles links 0.2 4 0.9]
  display
end
@#$#@#$#@
GRAPHICS-WINDOW
213
10
627
445
50
50
4.0
1
10
1
1
1
0
0
0
1
-50
50
-50
50
0
0
1
ticks
30.0

SLIDER
8
120
180
153
K-inputs
K-inputs
0
15
5
1
1
NIL
HORIZONTAL

SLIDER
8
84
180
117
N-nodes
N-nodes
1
100
24
1
1
NIL
HORIZONTAL

PLOT
656
163
929
313
Fitness
Iterations (ticks)
Fitness
0.0
10.0
0.0
1.0
true
true
"" ""
PENS
"Mean" 1.0 0 -13345367 true "" ""
"Max" 1.0 0 -16777216 true "" ""

SLIDER
8
48
180
81
number-of-turtles
number-of-turtles
1
200
200
1
1
NIL
HORIZONTAL

BUTTON
4
206
144
239
Setup small world
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
9
288
72
321
Go
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
656
316
736
361
Agent Mean
mean-fitness
3
1
11

MONITOR
739
316
812
361
Agent Max
max-fitness
3
1
11

PLOT
657
10
857
160
Fitness-Histogram
Fitness
# Agents
0.0
1.0
0.0
5.0
true
false
"" ""
PENS
"default" 1.0 1 -16777216 true "" ""

TEXTBOX
656
364
806
382
Initial Values:
11
0.0
1

MONITOR
655
382
735
427
Agent Mean
initial-mean-fitness
3
1
11

MONITOR
738
382
811
427
Agent Max
initial-max-fitness
3
1
11

MONITOR
656
454
736
499
Agent Mean
100 * ((mean-fitness / initial-mean-fitness) - 1)
1
1
11

TEXTBOX
660
435
810
453
% Improvement:
11
0.0
1

MONITOR
739
454
812
499
Agent Max
100 * ((max-fitness / initial-max-fitness) - 1)
1
1
11

BUTTON
79
288
145
321
Go Once
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
8
163
180
196
num-additional
num-additional
0
1000
0
1
1
NIL
HORIZONTAL

SLIDER
8
253
180
286
max-iterations
max-iterations
0
100000
4000
1
1
NIL
HORIZONTAL

SLIDER
9
336
181
369
prob-pref
prob-pref
0
1
1
0.01
1
NIL
HORIZONTAL

BUTTON
8
371
178
404
NIL
generate-ba-topology\n
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

@#$#@#$#@
## WHAT IS IT?

A model of innovation in a network topology. It is a fusion of Christopher J Watts' model of Stuart Kauffman's NK Fitness Landscapes http://www.simian.ac.uk/SimianResources/Book%20:%20Simulating%20Innovation%20-%20Models/5_SM/HeuristicSearch_KauffmanNK1.nlogo and the innovation model of Alan Friedman and David Lazer (2007)

## How fitness is assigned to a N bit string

The following is from Christopher J Watts description of the NK model, note that 'nodes' here refers to bits in the solution string, and not the nodes in the network): 
"There are N "nodes" in the search space. Each node has a binary variable, its current state. Each node takes input from K input nodes, plus itself. Each node has a fitness table, listing the contribution it makes to fitness given the current states of all its input nodes, including itself. Input nodes are assigned at randomly uniformly. Tables of fitness contributions are populated from a uniform distribution in the range [0, 1). Given a combination of all N node states, the N contributions can be averaged to compute a single fitness value."

## HOW TO USE IT

"setup-small-world" calls setup-nk to define the input tables and fitness tables.  
Then it constructs the network topology. A regular ring-lattice with NUMBER-OF-TURTLES nodes and connections between nearest neighbors. NUM-ADDITIONAL random edges are added on top of the lattice.

"setup-ba-topology" sets up a network that is grown randomly (PROB-PREF=0) or preferentially (PROB-PREF = 1). 
  
"go" has each agent doing the following:
Check if any of its network neighbors have a solution with higher fitness. If so, copy that solution. Otherwise flip one of the bits in its existing solution and see if it has higher fitness. If it does, then keep the new solution, otherwise keep the old solution.

## THINGS TO NOTICE
How does the presence of random edges affect the speed with which agents converge on a solution? How does it affect the fitness of the solution they converge to?

In improving their solution, the agents are flipping just one bit at a time. This may mean that they get stuck in a local optimum, from which flipping any one bit gives them worse fitness, but there may be an optimal solution somewhere else in the search space but more than 1 bit would need to be flipped in order to arrive there.

## CREDITS AND REFERENCES

This model uses several UI features and funcitons from Christopher J. Watts NetLogo model http://www.simian.ac.uk/SimianResources/Book%20:%20Simulating%20Innovation%20-%20Models/5_SM/HeuristicSearch_KauffmanNK1.nlogo

Kauffman, Stuart (1993) "The Origins of Order: Self-Organization and Selection in Evolution". New York: OUP

Kauffman, Stuart (1995) "At home in the universe: the search for laws of complexity". London: Penguin.

Kauffman, Stuart (2000) "Investigations". Oxford : Oxford University Press

Kauffman, Stuart, Jose Lobo & William G Macready (2000) "Optimal search on a technology landscape". Journal of Economic Behavior & Organization 43 141-166

David Lazer and Alan Friendman (2007), "The Network Structure of Explorationa and Exploitation", Administrative Science Quaterly, 52(4), p. 667-694.
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
0
Rectangle -7500403 true true 151 225 180 285
Rectangle -7500403 true true 47 225 75 285
Rectangle -7500403 true true 15 75 210 225
Circle -7500403 true true 135 75 150
Circle -16777216 true false 165 76 116

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.0.2
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="experiment-VarK" repetitions="100" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks = 2000</exitCondition>
    <metric>timer</metric>
    <metric>mean-fitness</metric>
    <metric>max-fitness</metric>
    <metric>initial-mean-fitness</metric>
    <metric>initial-max-fitness</metric>
    <enumeratedValueSet variable="K-inputs">
      <value value="0"/>
      <value value="1"/>
      <value value="2"/>
      <value value="3"/>
      <value value="4"/>
      <value value="5"/>
      <value value="6"/>
      <value value="7"/>
      <value value="8"/>
      <value value="9"/>
      <value value="10"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Output-Every">
      <value value="2000"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="N-nodes">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Number-of-Agents">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Max-ticks">
      <value value="500"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment" repetitions="50" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks = 50</exitCondition>
    <metric>timer</metric>
    <metric>count agents</metric>
    <metric>initial-mean-fitness</metric>
    <metric>initial-max-fitness</metric>
    <metric>mean-fitness</metric>
    <metric>max-fitness</metric>
    <metric>((mean-fitness / initial-mean-fitness) - 1)</metric>
    <metric>((max-fitness / initial-max-fitness) - 1)</metric>
    <metric>order-statistic</metric>
    <enumeratedValueSet variable="N-nodes">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Number-of-Agents">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Output-Every">
      <value value="50"/>
    </enumeratedValueSet>
    <steppedValueSet variable="Retention" first="5" step="10" last="95"/>
    <steppedValueSet variable="Selection" first="5" step="10" last="95"/>
    <steppedValueSet variable="K-inputs" first="0" step="1" last="9"/>
    <enumeratedValueSet variable="Max-ticks">
      <value value="500"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Opt-Method">
      <value value="&quot;Cross-Entropy Method&quot;"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment-RWHC" repetitions="50" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks = 50</exitCondition>
    <metric>timer</metric>
    <metric>count agents</metric>
    <metric>initial-mean-fitness</metric>
    <metric>initial-max-fitness</metric>
    <metric>mean-fitness</metric>
    <metric>max-fitness</metric>
    <metric>((mean-fitness / initial-mean-fitness) - 1)</metric>
    <metric>((max-fitness / initial-max-fitness) - 1)</metric>
    <metric>order-statistic</metric>
    <enumeratedValueSet variable="N-nodes">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Number-of-Agents">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Output-Every">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Retention">
      <value value="75"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Selection">
      <value value="5"/>
    </enumeratedValueSet>
    <steppedValueSet variable="K-inputs" first="0" step="1" last="9"/>
    <enumeratedValueSet variable="Max-ticks">
      <value value="500"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Opt-Method">
      <value value="&quot;Random-Walk Hill Climb&quot;"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment-CEM" repetitions="10" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks = 50</exitCondition>
    <metric>timer</metric>
    <metric>count agents</metric>
    <metric>initial-mean-fitness</metric>
    <metric>initial-max-fitness</metric>
    <metric>mean-fitness</metric>
    <metric>max-fitness</metric>
    <metric>((mean-fitness / initial-mean-fitness) - 1)</metric>
    <metric>((max-fitness / initial-max-fitness) - 1)</metric>
    <metric>order-statistic</metric>
    <enumeratedValueSet variable="Opt-Method">
      <value value="&quot;Cross-Entropy Method&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="N-nodes">
      <value value="20"/>
    </enumeratedValueSet>
    <steppedValueSet variable="K-inputs" first="0" step="1" last="9"/>
    <enumeratedValueSet variable="Number-of-Agents">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Heat-Retention">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Crossover">
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Mutation">
      <value value="0"/>
      <value value="1"/>
      <value value="2"/>
      <value value="4"/>
      <value value="8"/>
      <value value="16"/>
    </enumeratedValueSet>
    <steppedValueSet variable="Retention" first="5" step="10" last="95"/>
    <steppedValueSet variable="Selection" first="5" step="10" last="95"/>
    <enumeratedValueSet variable="Memory-Length">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Tabu-List-Length">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Output-Every">
      <value value="50"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Max-ticks">
      <value value="500"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment-HSS" repetitions="1000" runMetricsEveryStep="false">
    <setup>set memory-length int (100 / number-of-agents)
setup</setup>
    <go>go</go>
    <metric>timer</metric>
    <metric>count agents</metric>
    <metric>initial-mean-fitness</metric>
    <metric>initial-max-fitness</metric>
    <metric>mean-fitness</metric>
    <metric>max-fitness</metric>
    <metric>((mean-fitness / initial-mean-fitness) - 1)</metric>
    <metric>((max-fitness / initial-max-fitness) - 1)</metric>
    <metric>order-statistic</metric>
    <metric>memory-length</metric>
    <enumeratedValueSet variable="N-nodes">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="K-inputs">
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Number-of-Agents">
      <value value="1"/>
      <value value="2"/>
      <value value="4"/>
      <value value="5"/>
      <value value="10"/>
      <value value="20"/>
      <value value="25"/>
      <value value="50"/>
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Mutation">
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Crossover">
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Memory-Length">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Tabu-List-Length">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Heat-Retention">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Retention">
      <value value="80"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Selection">
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Output-Every">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Max-ticks">
      <value value="100"/>
      <value value="500"/>
      <value value="2000"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Opt-Method">
      <value value="&quot;Harmony Social Search&quot;"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 1.0 0.0
0.0 1 1.0 0.0
0.2 0 1.0 0.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@
