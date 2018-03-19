classdef FreeField_20170804_01_TetraOmni < FreeFieldArray
        properties (SetAccess=protected)
            % properties from ElobesMicArray
            sensorCartesianPositionsDefault
            refChan
    
        end
    methods
        function[obj] = FreeField_20170804_01_TetraOmni()
       
            % Use superclass to create the object
            obj = obj@FreeFieldArray();
            
            % Populate the parameters
            obj.sensorCartesianPositionsDefault = predefinedSensorPositions();
            obj.refChan = 1;  % reference is the origin
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