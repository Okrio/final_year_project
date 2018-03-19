classdef RigidSphere_20171102_01_horizontal_circle16 < RigidSphereArray & BinauralArray
    properties (SetAccess=protected)
        % properties from ElobesMicArray already implemented in SphericalHarmonicSoundFieldArray
        
        % properties from BinauralArray
        refChanLeft
        refChanRight
        channelsLeft
        channelsRight
    end
    methods
        function[obj] = RigidSphere_20171102_01_horizontal_circle16()
            
            % use superclass to create the object with input parameter
            obj = obj@RigidSphereArray(0.09);
            
            % override the default properties of the superclass
            obj.sensorCartesianPositionsDefault = predefinedSensorPositions();
            obj.refChan = 0; % reference is the origin
            
            % populate the parameters
            obj.refChanLeft = 1;
            obj.refChanRight = 2;
            obj.channelsLeft = (1:2:length(obj.sensorCartesianPositionsDefault-1)).';
            obj.channelsRight = (2:2:length(obj.sensorCartesianPositionsDefault)).';            
        end
    end

end

function[sensor_pos] = predefinedSensorPositions()
% evaluate to determine the postitions of the elements relative to
% the origin
nMics = 16;
radius = 0.1;     % radius on which microphones lie [metres]

% to make it binaural all mics should be asssigned to left or right so
% spacing should be symmetric about the median plane
angular_spacing = 2*pi/nMics;
az_left = angular_spacing/2 : angular_spacing : pi;
az_right = -az_left;

az = reshape([az_left;az_right],[],1);
inc = pi/2*ones(size(az));

sensor_pos = radius * [cos(az).*sin(inc), sin(az).*sin(inc), cos(inc)]; % [x,y,z] offsets of sensors
end