from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable, String, Time
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import datetime

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield u'Hello, %s' % name
            
    @rpc(Integer, Integer, Integer, Integer, Integer, Integer, _returns=String)
    def addition(ctx, DistanceKM, DistanceMetre, vitesse, autonomie, TempsDeChargementHeures, TempsDeChargementMinutes):
        #Pour les tests, vitesse de 100 km/h 
        
        distanceTotal = DistanceKM * 1000 + DistanceMetre
        
        TempsTotal = (distanceTotal/1000) / (vitesse)
        
        Test = (distanceTotal/1000) // (autonomie+1)
        heures=0
        minutes=0
        
        for i in range(int(Test)):
            heures = int(TempsTotal) + TempsDeChargementHeures
            minutes = int((TempsTotal % 1) * 60) + TempsDeChargementMinutes
            
            if (minutes >= 60):
                heures += (minutes // 60)
                minutes = minutes % 60
            
            STRTOMAKE = str(heures) + '.' + str(minutes)
            TempsTotal = float(STRTOMAKE)
           
        TempsTotal = f'{heures} h {minutes} minutes'
    
        return TempsTotal      
    
            
application = Application(
    [HelloWorldService],
    'spyne.examples.hello.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

server = make_server('127.0.0.1', 8001, wsgi_application)
server.serve_forever()

