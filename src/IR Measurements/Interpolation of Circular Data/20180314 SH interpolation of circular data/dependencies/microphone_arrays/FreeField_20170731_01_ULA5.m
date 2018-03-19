classdef FreeField_20170731_01_ULA5 < FreeFieldArray & BinauralArray
        properties (SetAccess=protected)
            % properties from ElobesMicArray
            sensorCartesianPositionsDefault
            refChan
    
            % properties from BinauralArray
            refChanLeft
            refChanRight
            channelsLeft
            channelsRight
        end
    methods
        function[obj] = FreeField_20170731_01_ULA5()
       
            % Use superclass to create the object
            obj = obj@FreeFieldArray();
            
            % Populate the parameters
            obj.sensorCartesianPositionsDefault = predefinedSensorPositions();
            obj.refChan = 3;  % reference is the origin
            obj.refChanLeft = 1;
            obj.refChanRight = 5;
            obj.channelsLeft = [1;2];
            obj.channelsRight = [4;5];
        end
    end
    
end

function[sensor_pos] = predefinedSensorPositions()
% evaluate to determine the postitions of the elements relative to
% the origin
% to number from left to right from listener perspective align with y-axis

x_pos = zeros(5,1);
y_pos = 0.05 * (2:-1:-2).';
z_pos = zeros(5,1);

sensor_pos = [x_pos,y_pos,z_pos]; % [x,y,z] offsets of sensors
end