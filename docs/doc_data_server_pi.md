*Last update on 25/04/2020*

# Data Server on Raspberry PI

## Smart Home Installation

I will decribe on this page a simple Smart Home Installation which I have build for my home. 


```plantuml
@startuml
    rectangle Raspberry_PI
    rectangle STM32
    cloud Internet
    rectangle Smartphone
    rectangle " Internal \n Temperature \n Sensor" as ITS
    rectangle " External \n Temperature \n Sensor"  as ETS
    rectangle VMC_Controller
    rectangle VMC

    Smartphone -- Internet 
    Internet -- Raspberry_PI
    Raspberry_PI -- STM32: USB
    STM32 -- ETS: 433MHz
    STM32 -- ITS: cable
    Raspberry_PI -- VMC_Controller: WiFi
    VMC_Controller -- VMC: 433MHz
@enduml
```

The installation is not limited on described modules and can be adapted for all particular uses.


## Demonstration

<img src="../images/img_doc_data_server_pi_demo.gif">


## Source Code 

Source code of this project: 

- [https://github.com/tuppi-ovh/data-server-stm32](https://github.com/tuppi-ovh/data-server-stm32)

- [https://github.com/tuppi-ovh/data-server-pi](https://github.com/tuppi-ovh/data-server-pi)



