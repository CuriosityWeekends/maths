> [!NOTE]
> This covers the theory behind the algorithm
> The idea is, to look at the min and max distance possible between the different routers

##O1 (Distance to routers from orgin1)
R1: 10
R2: 20
R3: 25
> We are given only these values
###Distance between each Routers
R1 --> R2: (|20 - 10|) `10 <> 30` (|20 + 10|)
R1 --> R3: (|25 - 10|) `15 <> 35` (|25 + 10|)
R2 --> R3: (|25 - 20|) `5 <> 45` (|25 + 20|)
> the idea of min distance is the smallest distance between the two diffrent routers distance from orgin (which is the diffrence)
> and max distance is the sum of the distance of the two routers distance from orgin
> so effectively we get a range of the possible Distances between routers
##O2 (Distance to routers from orgin2)
R1: 18.03
R2: 5
R3: 10
###Distance between each Routers
R1 --> R2: (|18.03 - 5|) `13.03 <> 23.03` (|18.03 + 5|)
R1 --> R3: (|18.03 - 10|) `8.03 <> 28.03` (|18.03 + 10|)
R2 --> R3: (|5 - 10|) `5 <> 15` (|5 + 10|)
##Total Conclusion With All datas
R1 --> R2: `13.03 <> 23.03`
R1 --> R3: `8.03 <> 28.03`
R2 --> R3: `5 <> 15`

> And as we continues to do it, the accuracy of the range becomes closer and closer to the actual distance, which is soo cool
> AND CHECK IT OUT IN ACTION WITH THE PYTHON SCRIPT `example1.py`
