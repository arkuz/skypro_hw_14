class Rating:
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG-13'
    R = 'R'
    NC_17 = 'NC-17'


class RatingGroup:
    CHILDREN = (Rating.G, )
    FAMILY = (Rating.G, Rating.PG, Rating.PG_13)
    ADULT = (Rating.R, Rating.NC_17)
