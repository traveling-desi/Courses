/*
 * 
 * Copyright 2014 Jules White
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 */

package org.magnum.mobilecloud.video;

import java.security.Principal;
import java.util.Collection;
import java.util.Set;

import javax.servlet.http.HttpServletResponse;

import org.magnum.mobilecloud.video.repository.Video;
import org.magnum.mobilecloud.video.repository.VideoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.google.common.collect.Lists;

@Controller
public class SpringController {
	
	public static final String DATA_PARAMETER = "data";
	public static final String ID_PARAMETER = "id";
	public static final String TITLE_PARAMETER = "title";
	public static final String DURATION_PARAMETER = "duration";
	public static final String VIDEO_SVC_PATH = "/video";
	public static final String VIDEO_ID_PATH = VIDEO_SVC_PATH + "/{id}";
	public static final String VIDEO_DATA_PATH = VIDEO_ID_PATH + "/data";
	public static final String VIDEO_LIKEDBY_PATH = VIDEO_ID_PATH + "/likedby";
	public static final String VIDEO_LIKE_PATH = VIDEO_ID_PATH + "/like";
	public static final String VIDEO_UNLIKE_PATH = VIDEO_ID_PATH + "/unlike";
	public static final String VIDEO_TITLE_SEARCH_PATH = VIDEO_SVC_PATH + "/search/findByName";
	public static final String VIDEO_DURATION_SEARCH_PATH = VIDEO_SVC_PATH + "/search/findByDurationLessThan";
	    
    @Autowired
    private VideoRepository videos;


    //  GET /video
	@RequestMapping(value=VIDEO_SVC_PATH, method=RequestMethod.GET)
	public @ResponseBody Collection<Video> getVideoList() {
		// TODO Auto-generated method stub
		return Lists.newArrayList(videos.findAll());
	}

	//  GET /video/{id}
	@RequestMapping(value=VIDEO_ID_PATH, method=RequestMethod.GET)
	public @ResponseBody Video getVideoByid(@PathVariable("id") long id, HttpServletResponse response) {
		// TODO Auto-generated method stub
	
		// TODO : Check if id is null. Need it to be Long ???		
		Video v = findVideoById(id);
		
		if (v != null) {
			return v;
		} else {
			response.setStatus(HttpServletResponse.SC_NOT_FOUND);
			return null;
		}
	}
	
	
	private Video findVideoById(long id) {
		return  videos.findOne(id);
	}
	
	
	//  GET /video/{id}/likedby
	@RequestMapping(value=VIDEO_LIKEDBY_PATH, method=RequestMethod.GET)
	public @ResponseBody Set<String> getVideoByLikedBy(@PathVariable("id") long id, HttpServletResponse response) {
		
		Video v = findVideoById(id);
		if (v != null) {
			return v.getLikedBy();
		} else {
			response.setStatus(HttpServletResponse.SC_NOT_FOUND);
			return null;
		}
	}
	
	// GET /video/search/findByName?title={title}
    @RequestMapping(value=VIDEO_TITLE_SEARCH_PATH, method=RequestMethod.GET)
    public @ResponseBody Collection<Video> findByTitle(
                    // Tell Spring to use the "title" parameter in the HTTP request's query
                    // string as the value for the title method parameter
                    @RequestParam(TITLE_PARAMETER) String name
    ){
            return videos.findByName(name);
    }
    
	

	// GET /video/search/findByDurationLessThan?duration={duration}
    @RequestMapping(value=VIDEO_DURATION_SEARCH_PATH, method=RequestMethod.GET)
    public @ResponseBody Collection<Video> findByDurationLessThan(
                    // Tell Spring to use the "title" parameter in the HTTP request's query
                    // string as the value for the title method parameter
                    @RequestParam(DURATION_PARAMETER) long duration 
    ){
    		return Lists.newArrayList(videos.findByDurationLessThan(duration));
    }
	
    
	// POST /video
	@RequestMapping(value=VIDEO_SVC_PATH, method=RequestMethod.POST)
	public @ResponseBody Video addVideo(@RequestBody Video v) {
		// TODO Auto-generated method stub
		v.setLikes(0);
		return videos.save(v);
	}
	

	// POST /video/{id}/like
	@RequestMapping(value=VIDEO_LIKE_PATH, method=RequestMethod.POST)
	public void addLike(@PathVariable("id") long id, HttpServletResponse response, Principal p) {
		// TODO Auto-generated method stub
		
		String username = p.getName();
		Video v = findVideoById(id);
		
		if (v != null) {
			Set<String> likedBy = v.getLikedBy();
			if (likedBy.contains(username)) 
				response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
			 else {
				v.setLikedBy(username);
				v.setLikes(v.getLikes() + 1);
				videos.save(v);
				response.setStatus(HttpServletResponse.SC_OK);
			 }
		} else 
			response.setStatus(HttpServletResponse.SC_NOT_FOUND);
	}
	
	// POST /video/{id}/unlike
	@RequestMapping(value=VIDEO_UNLIKE_PATH, method=RequestMethod.POST)
	public void addUnLike(@PathVariable("id") long id, HttpServletResponse response, Principal p) {
		// TODO Auto-generated method stub
		
		String username = p.getName();
		Video v = findVideoById(id);
		
		if (v != null) {
			Set<String> likedBy = v.getLikedBy();
			if (! likedBy.contains(username)) 
				response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
			 else {
				v.removeLikedBy(username);
				v.setLikes(v.getLikes() - 1);
				videos.save(v);
				response.setStatus(HttpServletResponse.SC_OK);
			 }
		} else 
			response.setStatus(HttpServletResponse.SC_NOT_FOUND);
	}
}
