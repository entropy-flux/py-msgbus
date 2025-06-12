from pytest import mark
from unittest.mock import Mock 
from pymsgbus.depends import inject, Depends, Provider

provider = Provider()

def left_leaf_dependency():
    return 2
    
async def right_leaf_dependency():
    return 3

async def right_node_dependency(leaf = Depends(right_leaf_dependency)):
    yield leaf*5

async def root_dependency(left = Depends(left_leaf_dependency), right = Depends(right_node_dependency)):
    return left*right*7

@inject(provider)
def handle_dependency(root = Depends(root_dependency)):
    return root*11

def test_handle_nested_depends():
    value = handle_dependency()
    assert value == 2*3*5*7*11

    provider.dependency_overrides[right_node_dependency] = lambda: 13
    value = handle_dependency()
    assert value == 2*7*11*13