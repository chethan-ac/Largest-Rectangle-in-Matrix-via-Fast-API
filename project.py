from typing import List, Tuple
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class MatrixRequest(BaseModel):
    matrix: List[List[int]]

class RectangleResponse(BaseModel):
    area: int
    number: int

def largest_rectangle_area(histo):
    st = []
    max_area = 0
    max_number = 0
    n = len(histo)

    for i in range(n + 1):
        while st and (i == n or histo[st[-1]] >= histo[i]):
            height = histo[st.pop()]
            width = i if not st else i - st[-1] - 1
            current_area = width * height
            if current_area > max_area:
                max_area = current_area
                max_number = height
        
        st.append(i)

    return max_area, max_number

def largest_rectangle(matrix: List[List[int]]) -> Tuple[int, int]:
    if not matrix or not matrix[0]:
        raise HTTPException(status_code=400, detail="Invalid matrix")

    rows, cols = len(matrix), len(matrix[0])
    max_area = 0
    max_number = 0
    histo = [0] * cols

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                histo[j] += 1
            else:
                histo[j] = 0
        
        area, number = largest_rectangle_area(histo)
        if area > max_area:
            max_area = area
            max_number = matrix[i][0]

    return max_area, max_number

@app.post("/largest_rectangle", response_model=RectangleResponse)
async def find_largest_rectangle(matrix_request: MatrixRequest) -> RectangleResponse:
    try:
        area, number = largest_rectangle(matrix_request.matrix)
        return RectangleResponse(area=area, number=number)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")