function is_in = test_if_points_in_ellipsoid_3d(pos, axis_dir, centre, r)
% Evalue whether a 3d point is inside a ellipsoid with axis direction
% axis_dir and radius r, the centre of the ellipsoid is at centre
% Input: pos (n*3)
%        centre (1*3)
%        axis_dir(3*3) each col (3*1) is one direction
%        r(1*3)
% Output: is_in: bool (n*1)
% 03/11/2021 rachel_sunrui

% -----------  Check input ------------------------------------------------
p = inputParser;

addRequired(p,'pos',@(x) isnumeric(x) & size(x,2) == 3);
addRequired(p,'axis_dir',@(x) isnumeric(x) & size(x,1) == 3 & size(x,2) == 3);
addOptional(p,'centre',[0, 0, 0], @(x) isnumeric(x) & size(x,2) == 3);
addOptional(p,'r',[1, 1, 1],@(x) isnumeric(x) & size(x,2) == 3)
parse(p, pos, axis_dir, centre, r)
pos = p.Results.pos;
axis_dir = p.Results.axis_dir;
centre = p.Results.centre;
r = p.Results.r;
% Make sure axis is perpendicular 
test_axis_dir = reshape(axis_dir(:, [1,2,1,3,2,3]),3,2,3);
v = squeeze(sum(test_axis_dir(:,1,:).*test_axis_dir(:,2,:),1));
if sum(v)>1e-6
    error('Check axis_dir')
end
axis_dir = axis_dir./sum(axis_dir.^2,1);

% ----- Space transform and check if it is in the ellipsoid ---------------
new_pos = (axis_dir'*(pos-centre)')';
is_in = sum((new_pos.^2)./r.^2, 2)<1;
end

