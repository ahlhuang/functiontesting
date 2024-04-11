from functions import *
from requests import ConnectionError

obj_definition = {
    "top": 5,
    "left": 6,
    "width": 10,
    "height": 12,
    "scaleX": 2,
    "scaleY": 3,
    "angle": 15
}

def test_obj_rect2coords():
    res = obj_rect2coords(obj_definition)
    assert res == (5, 6, 20, 36, 15)

def test_compute_affine():
    dsize = (10, 20)
    frame_affine_matrix= np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    affine = compute_affine(obj_definition, dsize, frame_affine_matrix)
    expected = np.array([[ 4.82962938e-01,  1.29409522e-01, -3.54482524e+00],
       [-1.43788338e-01,  5.36625438e-01, -1.82039716e+00],
       [ 3.31136874e-10, -5.73546014e-10,  1.00000000e+00]])
    assert np.allclose(affine, expected, atol=1e-5)

def test_draw_edge_locs():
    frame = np.zeros((10, 10, 3), dtype=np.uint8)
    edge_locs = [(2, 3), (5, 7), (8, 1)]
    result_frame = draw_edge_locs(frame.copy(), edge_locs)
    for loc in edge_locs:
        assert np.array_equal(result_frame[loc[1], loc[0]], np.array([255, 0, 0]))

def test_hex2bgr():
    hex_color = "#FF5733"
    bgr = hex2bgr(hex_color)
    assert bgr == (51, 87, 255)

def test_bgr2hex():
    bgr = (51, 87, 255)
    hex_color = bgr2hex(bgr)
    assert hex_color == "#FF5733"

def test_is_port_open(mocker):
    mock = mocker.Mock()
    mocker.patch("socket.socket", return_value=mock)
    mock.connect.return_value = None
    assert is_port_open("127.0.0.1", 80) == True
    mock.connect.assert_called_once()
    mock.shutdown.assert_called_once()
    mock.reset_mock()
    mock.connect.side_effect = Exception("Port is closed")
    assert is_port_open("127.0.0.1", 80) == False
    mock.connect.assert_called_once()
    mock.shutdown.assert_not_called()


def test_wait_for_service(mocker):
    mock_get = mocker.patch("requests.get")
    mock_fail = mocker.Mock()
    mock_fail.raise_for_status.side_effect = ConnectionError
    mock_pass = mocker.Mock()
    mock_pass.status_code = 200
    mock_get.side_effect = [mock_fail, mock_pass]
    wait_for_service()
    assert mock_get.call_count == 2