# the neural network used has accuracy  0.9517 and consist of:
    - Conv2D with 50 filter with size(3, 3) 
    - MaxPool2D with size of (2, 2)
    - another Conv2D with 50 filter with size(3, 3)
    - another MaxPool2D with size of (2, 2) then flatting
    - two hidden layers with 128 unit
    - dropout: (0.5)
    
# the process :

### changing the hidden layers
     1- first attempt : using the same neural network as in lecture result in accuracy: .0564
        
    2- second attempt : by adding two hidden layer with 128 uint to the network accuracy: .9328 (huge improve)
        
     3- third attempt : by adding  one hidden layer with 128 uint to the network accuracy: .5903
     
**just one layer does not work so use two hidden layer of size 128 unit
               
### using two hidden layer and changing the filter count
     increasing the filler count from 32 --> 50  accuracy change from .5903 to .8758
        
### using two hidden layer and 50 filter and changing the pool_size
     changing the pool_size from (2,2) to (3,3) lower the accuracy from .8758 to .6116
        
### using two hidden layer and 50 filter and pool_size = (2,2)
     changing the dropout from .5 to .7 lower the accuracy to 0.3682
     changing the dropout from .5 to .3 lower the accuracy to 0.8108
        
### adding another round of Conv2D and pooling
        * improve the accurse from .8758 to 9517 *_*


  