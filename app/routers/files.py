from fastapi import APIRouter, UploadFile


router = APIRouter()


@router.post('/upload')
async def upload_file(
    file: UploadFile,
):
    # save file in public folder
    with open(f'public/{file.filename}', 'wb') as f:
        f.write(file.file.read())
    return {'filename': file.filename}
