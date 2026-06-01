from fastapi import FastAPI

# creating API instance
app = FastAPI()

# async tells the computer it will have to wait on another file to
# finish before it can continue, but can work on something else in
# the meantime


@app.get('/')
async def root():
    '''This is a test to see redoc changes'''
    return {'message': 'This is the second test'}
# requires bash $fastapi dev to start development server
