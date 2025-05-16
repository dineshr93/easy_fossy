"""
This module provides compatibility between pydantic v1 and v2 models.

It helps bridge the differences in API between the versions, particularly for:
- RootModel vs __root__ fields
- Model validation and creation
- Serialization and deserialization
"""

import sys
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast
from pydantic import BaseModel, ConfigDict, RootModel

T = TypeVar('T', bound=BaseModel)

def ensure_root_model(cls: Type[T]) -> Type[T]:
    """
    Decorator to ensure a model with __root__ is compatible with pydantic v2
    
    Example:
        @ensure_root_model
        class MyRootModel(BaseModel):
            __root__: List[str]
    """
    if hasattr(cls, "__pydantic_decorators__"):
        # This is already a v2 model
        return cls
    
    # Check if this is a v1 model with __root__
    if hasattr(cls, "__fields__") and "__root__" in getattr(cls, "__fields__", {}):
        # Create a new RootModel class
        root_type = cls.__fields__["__root__"].type_
        
        class WrappedRootModel(RootModel):
            model_config = ConfigDict(arbitrary_types_allowed=True)
            root: root_type
            
        # Copy metadata from original class
        WrappedRootModel.__name__ = cls.__name__
        WrappedRootModel.__doc__ = cls.__doc__
        
        return cast(Type[T], WrappedRootModel)
    
    return cls

def convert_model_data(data: Any) -> Any:
    """Convert RootModel data to appropriate format for compatibility"""
    if hasattr(data, "root"):
        # This is a v2 RootModel
        return data.root
    
    if isinstance(data, list):
        return [convert_model_data(item) for item in data]
    
    if isinstance(data, dict):
        return {k: convert_model_data(v) for k, v in data.items()}
    
    if hasattr(data, "model_dump"):
        # This is a v2 BaseModel
        return data.model_dump()
    
    if hasattr(data, "dict"):
        # This is a v1 BaseModel
        return data.dict()
    
    return data 