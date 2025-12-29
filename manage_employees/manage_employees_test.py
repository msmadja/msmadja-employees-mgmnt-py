import pytest
import mongomock
from unittest.mock import patch
from manage_employees import (ManageEmployeesRequest, Employee, QueryEmployeesRequest)
from manage_employees.types import Employee, DeleteEmployee, QueryEmployeesFilters
from .manage_employees import service


@pytest.fixture(autouse=True)
def mongo_client():
    from core.db.mongo import get_client
    get_client.cache_clear()
    client = mongomock.MongoClient()
    # Mock get client (which imported from core.db.mongo)
    with patch("core.db.mongo.get_client", return_value=client):
        yield client
    get_client.cache_clear()
    client.close()


def test_should_create_a_employee():
    # Employee creation
    employee = Employee(name="Yosi Yosian", employee_code= "23456", salary=10000)
    creationRequest = ManageEmployeesRequest(create=employee)
    service.manageEmployees(creationRequest)

    # Employee query and check
    queryRequest =  QueryEmployeesRequest(filters=QueryEmployeesFilters(employee_code="23456"))
    results = service.queryEmployees(request=queryRequest)

    assert len(results.data) == 1
    
    e = results.data[0];
    assert e.name == "Yosi Yosian";
    assert e.employee_code == '23456'
    assert e.salary == 10000


def test_should_delete_a_employee():
    # Create employee
    creationRequest = ManageEmployeesRequest(create=Employee(name="Yosi Yosian", employee_code= "23456", salary=10000))
    service.manageEmployees(creationRequest)

    # Employee query and check
    queryRequest =  QueryEmployeesRequest(filters=QueryEmployeesFilters(employee_code="23456"))
    results = service.queryEmployees(request=queryRequest)

    assert len(results.data) == 1

    # Delete employee by employee code
    deletionRequest = ManageEmployeesRequest(delete=DeleteEmployee(employee_code='23456'))
    service.manageEmployees(deletionRequest)

    # Employee query and check
    queryRequest =  QueryEmployeesRequest(filters=QueryEmployeesFilters(employee_code="23456"))
    results = service.queryEmployees(request=queryRequest)

    assert len(results.data) == 0


def test_should_query_with_limit():
    # Create first employee
    firstEmployeeCreation = ManageEmployeesRequest(create=Employee(name="Yosi Yosian", employee_code= "23456", salary=10000))
    service.manageEmployees(firstEmployeeCreation)

    # Create second employee 
    secondEmployeeCreation = ManageEmployeesRequest(create=Employee(name="Israel Israeli", employee_code= "34567", salary=10000))
    service.manageEmployees(secondEmployeeCreation)

   # Employees query and check
    queryRequest =  QueryEmployeesRequest(limit=1)
    results = service.queryEmployees(request=queryRequest)
    
    assert len(results.data) == 1;
    e = results.data[0];
    assert e.name == "Yosi Yosian";
    assert e.employee_code == '23456'
    assert e.salary == 10000


def test_should_query_with_skip():
    # Create first employee
    firstEmployeeCreation = ManageEmployeesRequest(create=Employee(name="Yosi Yosian", employee_code= "23456", salary=10000))
    service.manageEmployees(firstEmployeeCreation)

    # Create second employee 
    secondEmployeeCreation = ManageEmployeesRequest(create=Employee(name="Israel Israeli", employee_code= "34567", salary=10000))
    service.manageEmployees(secondEmployeeCreation)

   # Employees query and check
    queryRequest =  QueryEmployeesRequest(skip=1)
    results = service.queryEmployees(request=queryRequest)
    
    assert len(results.data) == 1;
    
    e = results.data[0];
    assert e.name == "Israel Israeli";
    assert e.employee_code == '34567'
    assert e.salary == 10000


