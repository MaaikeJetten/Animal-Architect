from variables import *


def JSONDetections(detections):
    minX = detections[0][0]
    startIndex = 0

    for index in range(len(detections)):
        det = detections[index]
        if detections[index][0] < minX:
            minX = detections[index][0]
            startIndex = index

    minDistance = 10000

    # array to make sure only next tokens are being looked at
    doneIndexes = []
    distances = []
    reliability_scores = []
    min_reliability = 0.5
    final_ids = []
    final_sign = False
    first_ids = []
    first_sign = False

    name_token = 0
    token_type = ""
    oldLevel = False
    new = 0
    multipleDetections = False
    closestIndex = 0

    # start with most left index
    doneIndexes.append(startIndex)
    distances.append(0)

    newIndex = startIndex

    # go through all tokens and check which is closest
    for i in range(len(detections)):
        id_token = 0
        distance_level = 1
        # use the token that was closest to the token in the previous round
        detNew = detections[newIndex]
        for index in range(len(detections)):
            # check the token has not been used before and index not in skipIndexes:
            if index not in doneIndexes:
                det = detections[index]
                newDistance = ((detNew[0] - det[0])**2 + (detNew[1] - det[1])**2)**0.5
                #check if new distance is actually the smallest
                if newDistance < minDistance:
                    if newDistance < 10:
                        multipleDetections = True
                    else:
                        multipleDetections = False
                    closestIndex = index
                    minDistance = newDistance
                    # to not repeat final loop
                    new = 1
        if new == 1:
            doneIndexes.append(closestIndex)
            closestClass = detections[closestIndex][3]
            nameLabel = str(labels[int(detections[closestIndex][3])])
            reliability = str(detections[closestIndex][2])
            for token in numbers:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "numbers"
            for token in multi:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "multi"
            for token in length:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "length"
            for token in area:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "area"
            for token in volume:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "volume"
            
            if multipleDetections and not oldLevel:
                first_ids.append(i)
            elif oldLevel and not multipleDetections:
                final_ids.append(i)
            distances.append(minDistance)
        if i == len(detections)-1:
            if oldLevel:
                final_ids.append(i)
        # start next loop with this found token
        oldLevel = multipleDetections
        newIndex = closestIndex
        minDistance = 10000
        new = 0

    json_tokens = '['
    for i in range(len(doneIndexes)):
        id_token = 0
        nameLabel = str(labels[int(detections[doneIndexes[i]][3])])
        reliability = str(detections[doneIndexes[i]][2])
        for token in numbers:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "numbers"
        for token in multi:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "multi"
        for token in length:
                if token["name"].lower() == nameLabel:
                    name_token = token["name"]
                    token_type = "length"
        for token in area:
            if token["name"].lower() == nameLabel:
                name_token = token["name"]
                token_type = "area"
        for token in volume:
            if token["name"].lower() == nameLabel:
                name_token = token["name"]
                token_type = "volume"
        
        for final in final_ids:
            if i == final:
                final_sign = True
                break
            else:
                final_sign = False
        for first in first_ids:
            if i == first:
                first_sign = True
                break
            else:
                first_sign = False
        
        if first_sign:
            json_tokens += '{"name":"onbekend","reliability":1.1,"type":"onbekend", "options": ['
        
        json_tokens += '{"name":"'+name_token+'","reliability":'+reliability+',"type":"'+token_type +'"}'
        
        if final_sign:
            json_tokens += ']}'
        
        if i != len(doneIndexes)-1: 
            json_tokens += ','
        
        print(str(id_token) + " : " + nameLabel + " : " + str(detections[doneIndexes[i]][2]) + " : " + str(distances[i]))

    json_tokens += ']'

    return json_tokens

def JSONOPDetections(detections):

    widthBoard = 0.0
    heightBoard = 0.0
    boardIndex = 0.0
    widthArea = 0.0
    heightArea = 0.0
    areaIndex = 0.0

    minX = detections[0][0]
    startIndex = 0

    for index in range(len(detections)):
        det = detections[index]
        if detections[index][5] == 1:
            widthBoard = detections[index][2]
            heightBoard = detections[index][3]
            boardIndex = index
        if detections[index][5] == 2:
            widthArea = detections[index][2]
            heightArea = detections[index][3]
            areaIndex = index
        if detections[index][0] < minX and detections[index][5] == 0:
            minX = detections[index][0]
            startIndex = index

    minDistance = 10000

    # array to make sure only next tokens are being looked at
    doneIndexes = [boardIndex, areaIndex]
    distances = [0,0]
    reliability_scores = []
    min_reliability = 0.5
    final_ids = []
    final_sign = False
    first_ids = []
    first_sign = False

    name_token = 0
    token_type = ""
    oldLevel = False
    new = 0
    multipleDetections = False
    closestIndex = 0

    # start with most left index
    doneIndexes.append(startIndex)
    distances.append(0)

    newIndex = startIndex

    # go through all tokens and check which is closest
    for i in range(len(detections)):
        id_token = 0
        distance_level = 1
        # use the token that was closest to the token in the previous round
        detNew = detections[newIndex]
        for index in range(len(detections)):
            # check the token has not been used before and index not in skipIndexes:
            if index not in doneIndexes:
                det = detections[index]
                newDistance = ((detNew[0] - det[0])**2 + (detNew[1] - det[1])**2)**0.5
                #check if new distance is actually the smallest
                if newDistance < minDistance:
                    if newDistance < 10:
                        multipleDetections = True
                    else:
                        multipleDetections = False
                    closestIndex = index
                    minDistance = newDistance
                    # to not repeat final loop
                    new = 1
        if new == 1:
            doneIndexes.append(closestIndex)
            closestClass = detections[closestIndex][5]
            nameLabel = str(labelsOP[int(detections[closestIndex][5])])
            reliability = str(detections[closestIndex][4])
            
            if multipleDetections and not oldLevel:
                first_ids.append(i)
            elif oldLevel and not multipleDetections:
                final_ids.append(i)
            distances.append(round(minDistance, 3))
        if i == len(detections)-1:
            if oldLevel:
                final_ids.append(i)
        # start next loop with this found token
        oldLevel = multipleDetections
        newIndex = closestIndex
        minDistance = 10000
        new = 0

    json_tokens = '['
    for i in range(len(doneIndexes)):
        id_token = 0
        nameLabel = str(labelsOP[int(detections[doneIndexes[i]][5])])
        reliability = str(detections[doneIndexes[i]][4])
        
        for final in final_ids:
            if i == final:
                final_sign = True
                break
            else:
                final_sign = False
        for first in first_ids:
            if i == first:
                first_sign = True
                break
            else:
                first_sign = False
        
        if first_sign:
            json_tokens += '{"name":"onbekend","reliability":1.1,"type":"onbekend", "options": ['
        
        json_tokens += '{"name":"'+nameLabel+'","reliability":'+reliability+',"distance":'+str(distances[i])+',"boardWidth":'+str(heightBoard)+',"areaWidth":'+str(heightArea)+'}'
        
        if final_sign:
            json_tokens += ']}'
        
        if i != len(doneIndexes)-1: 
            json_tokens += ','
        
        print(str(id_token) + " : " + nameLabel + " : " + str(detections[doneIndexes[i]][4]) + " : " + str(distances[i]))
    

    json_tokens += ']'

    return json_tokens

