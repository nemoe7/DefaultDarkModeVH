#version 150

#define LUMI(rgb) dot(vec3(0.2126,0.7152,0.0722),rgb)
#define BEZIER(t,p_0,p_1,p_x) (pow((1 - t),2.0)*p_0+2.0*((1-t)*t)*p_x+pow(t,2.0)*p_1)

#define M1_P_0 vec3(0.0, 0.0, 0.0)
#define M1_P_1 vec3(104.0/255.0)
#define M1_P_X vec3(47.0/255.0)

in vec4 vertexColor;
in float depthLevel;

uniform vec4 ColorModulator;

out vec4 fragColor;

void main() {
    vec4 color = vertexColor;
    if (color.a == 0.0) {
        discard;
    }

	if (color.a == 1) {
      if (depthLevel == 0) {
        if (color.r == color.g && color.r == color.b) {
          float t = LUMI(color.rgb);
		  vec3 new_color = BEZIER(t,M1_P_0,M1_P_1,M1_P_X);
		  color = vec4(new_color.r, new_color.g, new_color.b, 1.0);
        }
      }
    } else if (color.a == 128.0/255.0) {
	  color.a = 75.0/255.0;
    }

    fragColor = color * ColorModulator;
}
