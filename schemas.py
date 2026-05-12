from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class StatSchema(BaseModel):
    id: Optional[int] = None
    label: str
    value: str
    trend: str
    trendType: str

class OperationSummarySchema(BaseModel):
    id: Optional[int] = None
    label: str
    value: int
    sub: str
    badge: str
    badgeColor: str

class RecentOperationSchema(BaseModel):
    ref: str
    type: str
    typeColor: str
    item: str
    qty: str
    status: str
    statusColor: str
    date: str
    # Using 'from' and 'to' as field names directly
    # But 'from' is a reserved keyword in Python, so we use aliases for validation
    from_val: Optional[str] = Field(None, alias="from")
    to_val: Optional[str] = Field(None, alias="to")
    
    model_config = ConfigDict(populate_by_name=True)

class RecentOperationCreate(BaseModel):
    ref: str
    type: str
    type_color: str
    from_loc: str
    to_loc: str
    item: str
    qty: str
    status: str
    status_color: str
    date: str

class ProductSchema(BaseModel):
    sku: str
    name: str
    category: str
    categoryColor: str
    branch: str
    onHand: float
    unit: str
    forecast: float
    rule: str
    price: str
    status: str
    statusColor: str
    progress: int
    reorderDate: Optional[str] = None
    reorderQty: float = 0.0

class ProductUpdate(BaseModel):
    on_hand: Optional[float] = None
    reorder_date: Optional[str] = None
    reorder_qty: Optional[float] = None

class TransferRequest(BaseModel):
    from_branch: str
    to_branch: str
    product_sku: str
    quantity: float

class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    category_color: str
    branch: str
    on_hand: float
    unit: str
    forecast: float
    rule: str
    price: str
    status: str
    status_color: str
    progress: int

class ForecastSchema(BaseModel):
    day: str
    value: int
    color: str
    border: Optional[str] = None
    desc: str

class BranchSchema(BaseModel):
    name: str
    loc: str
    status: str
    statusColor: str
    capacity: str
    items: int
    value: str
    score: str
    util: int
    utilDesc: str

class AIReplySchema(BaseModel):
    question: str
    reply: str
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    name: str
    role: Optional[str] = "Manager"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True

class DashboardDataSchema(BaseModel):
    stats: List[StatSchema]
    operations: List[OperationSummarySchema]
    recentOperations: List[RecentOperationSchema]
    products: List[ProductSchema]
    forecast: List[ForecastSchema]
    branches: List[BranchSchema]
    aiReplies: List[AIReplySchema]
