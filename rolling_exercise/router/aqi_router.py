from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controller.quality_controller import insert_data_from_csv, get_qaulity_by_date, get_quality_by_city
import schemas
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd
from io import StringIO
from fastapi.responses import JSONResponse

