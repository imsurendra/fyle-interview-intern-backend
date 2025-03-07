def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_post_edit_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST Changed'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 2,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_post_bad_assignment_student_1(client, h_student_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    content = 'ABCD TESTPOST Changed'
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id": 100000,
            'content': content
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'

def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

def test_post_submitted_assignment_student_1(client, h_student_1):
    """
    failure case: Assignment can only be edited before submission
    """
    content = 'ABCD TESTPOST Changed Again'
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            "id": 2,
            'content': content
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_assingment_resubmitt_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
