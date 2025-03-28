import numpy as np
import cv2

class LineDetection:
    def __init__(self,edged):
        self.edged = edged
    
    def hough_line_transform(self,threshold,edge_coordinates):
        diagonal_length = np.ceil(np.sqrt(self.edged.shape[0]**2 + self.edged.shape[1]**2))
        
        theta_values = np.deg2rad(np.arange(-90,90,1))
        r_values = np.arange(-diagonal_length,diagonal_length+1,1)
        
        m,n = len(r_values),len(theta_values)
         
        accumulator = np.zeros((m,n))
        
        costhetas = np.cos(theta_values)
        sinthetas = np.sin(theta_values)
        
        for x,y in zip(edge_coordinates[0],edge_coordinates[1]):
            for theta in range(n):
                r = x*costhetas[theta] + y*sinthetas[theta]
                r_idx = np.where(r > r_values)[0][-1]
                accumulator[r_idx,theta] += 1
        
        final_r_idx,final_theta_idx = np.where(accumulator>threshold)
        final_r_values = r_values[final_r_idx]
        final_theta_values = theta_values[final_theta_idx]
        
        return final_r_values,final_theta_values
    
    def polar2cartesian(self,radius: np.ndarray, angle: np.ndarray, cv2_setup: bool = True) -> np.ndarray:
        return radius * np.array([np.sin(angle), np.cos(angle)])

    def distance_between_lines(self,pt1, pt2, pt3, pt4):

        m1 = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
        
        m2 = (pt4[1] - pt3[1]) / (pt4[0] - pt3[0])
        
        b1 = pt1[1] - m1 * pt1[0]
        b2 = pt3[1] - m2 * pt3[0]
        
        distance = np.abs(b1 - b2) / np.sqrt(m1**2 + 1)
        
        return distance
    
    
    
        
    def lineDetection(self,img_path):
        edge_coordinates = np.where(self.edged==255)
        
        threshold = 50
        i=0
        j=0
        
        output_image = np.zeros((self.edged.shape[0],self.edged.shape[1]))
        
        while(1):
            i = j
            final_r , final_theta = self.hough_line_transform(threshold, edge_coordinates)

            lines = []

            distance = 100
            
            new_img = cv2.imread(img_path)
            if (new_img.shape[0]>1000 or new_img.shape[1]>1000):
                new_img = cv2.resize(new_img, (0, 0), fx=0.3, fy=0.3)
                
            # print(np.argwhere(final_theta>1))
            
            for rho,theta in zip(final_r,final_theta):
                if -1<theta<1:
                    x0 = self.polar2cartesian(rho, theta)
                    # print(x0)
                    direction = np.array([x0[1], -x0[0]])
                    # print(direction)
                    pt1 = np.round(x0 + 1000*direction).astype(int)
                    pt2 = np.round(x0 - 1000*direction).astype(int)
                    line = [pt1,pt2]
                    if(lines!=[]):
                        for ln in lines:
                            pt3,pt4 = ln
                            distance = self.distance_between_lines(pt1,pt2,pt3,pt4)
                            if(distance<25):
                                # print("distance: "+str(distance))
                                break
                                
                    if(distance>25):     
                        lines.append([pt1,pt2])
                        cv2.line(new_img,pt1=pt1, pt2=pt2, color=[0,255,0], thickness=2)
                        i += 1
                if(i>15):
                    threshold += 50
                    j = 0
                    break
            
            if(i<=15):
                output_image = np.copy(new_img)
                break
                
                
        
        # print(lines)
        cv2.putText(output_image, "Stair number:" + str(i), (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        print(f"no of lines drawn : {i}")
        return output_image,i