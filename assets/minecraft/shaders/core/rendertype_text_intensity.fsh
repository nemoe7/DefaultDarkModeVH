#version 150

#moj_import <fog.glsl>

#define EQ(x,y) (distance(x, y) < 0.002)
#define MAP(a,b) if EQ(color.rgb, a) color.rgb = b;
#define MAPA(a,b) if EQ(color.rgba, a) color.rgba = b;
#define MAPIF(x,a,b) if (x && EQ(color.rgb, a)) color.rgb = b;

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in float depthLevel;

out vec4 fragColor;

void main() {
	vec4 color = vertexColor;

	MAPIF(	(depthLevel != 0.03 && depthLevel != 400),	vec3(0.248),	vec3(0.92)) else
	if (depthLevel == 0) {
	  MAP(	vec3(0.403,	0.3642,	0.2867),		vec3(0.72, 0.92, 0.52)		) else
	  MAP(	vec3(0.496),						vec3(0.87)					) else
	  MAP(	vec3(0.527),						vec3(0.92)					) else
	  MAP(	vec3(0.372),						vec3(0.86, 0.9, 0.9)		) else
	  MAP(	vec3(0.2635),						vec3(0.92, 0.87, 0.87)		) else
	  MAP(	vec3(0.3294),						vec3(0.78, 0.83, 0.87)		) else
	  MAP(	vec3(0.4883),						vec3(0.86, 0.9, 0.9)		) else
	  MAP(	vec3(0.0968),						vec3(0.86, 0.87, 0.9)		) else
	  MAP(	vec3(0.0968, 0.124, 0.1317),		vec3(0.86, 0.87, 0.9)		) else
	  MAP(	vec3(0.2867, 0.248, 0.1705),		vec3(0.9, 0.92, 0.7)		) else
	  MAP(	vec3(0.3991, 0.3604, 0.2829),		vec3(0.63, 0.83, 0.42)		) else
	  MAP(	vec3(0.279, 0.279, 0.2751),			vec3(0.87, 0.87, 0.85)		) else
	  MAP(	vec3(0.1162),						vec3(0.87, 0.85, 0.87)		) else
	  MAP(	vec3(0.3449, 0.1395, 0.1395),		vec3(0.92)					) else
	  MAP(	vec3(0.0542, 0.1317, 0.1976),		vec3(0.92)					) else
	  MAP(	vec3(0.31),							vec3(0.92)					) else
	  MAP(	vec3(0.6588),						vec3(0.92)					) else
	  MAP(	vec3(0.2325),						vec3(0.92)					) else
	  MAP(	vec3(0.186),						vec3(0.92)					) else
	  MAP(	vec3(0.4611),						vec3(0.92)					) else
	  MAP(	vec3(0.5929),						vec3(0.83)					) else
	  MAP(	vec3(0.1201, 0.2131, 0.2441),		vec3(0.92)					) else
	  MAP(	vec3(0.1743, 0.2441, 0.279),		vec3(0.83, 0.92, 0.92)		) else
	  MAP(	vec3(0.2441, 0.3216, 0.3526),		vec3(0.92, 0.87, 0.87)		) else
	  MAP(	vec3(0.4805, 0.5309, 0.5386),		vec3(0.9, 0.92, 0.92)		) else
	  MAPA(	vec4(0.0, 0.0, 0.0, 0.4),			vec4(0.92, 0.92, 0.92, 0.8)	)
	} else if (depthLevel == 0.03) {
	  MAP(	vec3(0.5929),						vec3(0.92)					) else
	  MAPA(	vec4(1.0),							vec4(0.0, 0.0, 0.0, 1.0)					)
	} else if (depthLevel == 1) {
	  MAP(	vec3(0.3294),						vec3(0.78, 0.83, 0.87)		)
	} else if (depthLevel == 2) {
	  color.rgb = vec3(0.83);
	} else if (depthLevel == 2.1) {
	  color.rgb = vec3(0.0);
	} else if (depthLevel == 500) {
	  MAP(	vec3(0.062),						vec3(0.83)					)
	} else if (depthLevel == 300) {
	  MAP(	vec3(0.4728),						vec3(0.74)					) else
	  MAP(	vec3(0.465),						vec3(0.83)					)
	} else MAP(	vec3(0.465),					vec3(0.83)					)

    color = vec4(vec3(1.0), texture(Sampler0, texCoord0).r) * color * ColorModulator;
	if (color.a < 0.1) discard;
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
