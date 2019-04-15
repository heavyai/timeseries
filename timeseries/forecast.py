import logging
import sys
import signal
import time
import subprocess

from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import python as python_deployer

from _ops import apply_forecast_impl

def signal_handler(signal, frame):
   logging.info("\nGracefully stopping server...")
   conn = ClipperConnection(DockerContainerManager())
   conn.stop_all()
   sys.exit(0)

def do_forecast(parameters):
    logging.info("\nForecast request: {}\n".format(parameters))
    try:
        response = apply_forecast_impl(parameters[0].decode("utf-8").split(','))
        code = '202' 
    except Exception as e:
        response = str(e)
        code = '500'
    return [str(code+', '+response) for _ in parameters]

if __name__ == '__main__':
    # setup logging format
    format = "%(asctime)-15s %(message)s"
    logging.basicConfig(
        filename='./timeseries/log.log', level=logging.DEBUG, format=format)
    # set up logging to console
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.ERROR)
    logging.getLogger().addHandler(console)

    signal.signal(signal.SIGINT, signal_handler)
    conn = ClipperConnection(DockerContainerManager())
    conn.start_clipper()
    try:
        conn.register_application(name="forecast",input_type="strings",default_output="500, Error executing call.",slo_micros=100000000)
        python_deployer.deploy_python_closure(conn, name="do-forecast", version=1, input_type="strings", func=do_forecast, base_image='wamsiv/timeseries')
        conn.link_model_to_app(app_name="forecast", model_name='do-forecast')
        print(subprocess.getoutput(["docker update --restart=on-failure $(docker ps -a | grep 'clipper/query_frontend:0.3.0' | awk '{ print $1 }')"]))
        input("Server started. Press ctrl+c to stop server.\n")
    except Exception as e:
        logging.error("Encountered {}. Stopping server...".format(e))
        conn.stop_all()
    conn.stop_all()
