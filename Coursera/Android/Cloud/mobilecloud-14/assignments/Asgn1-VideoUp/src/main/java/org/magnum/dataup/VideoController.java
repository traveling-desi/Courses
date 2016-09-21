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
package org.magnum.dataup;

import java.io.IOException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.magnum.dataup.model.Video;
import org.magnum.dataup.model.VideoStatus;
import org.magnum.dataup.model.VideoStatus.VideoState;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class VideoController {
	
	public static final String DATA_PARAMETER = "data";
	public static final String ID_PARAMETER = "id";
	public static final String VIDEO_SVC_PATH = "/video";
	public static final String VIDEO_DATA_PATH = VIDEO_SVC_PATH + "/{id}/data";
	
	private Map<Long,Video> videos = new HashMap<Long, Video>();
	
    private static final AtomicLong currentId = new AtomicLong(0L);
	
//	@Autowired
//	private VideoFileManager vMgr ;

	@RequestMapping(value=VIDEO_SVC_PATH, method=RequestMethod.GET)
	public @ResponseBody Collection<Video> getVideoList() {
		// TODO Auto-generated method stub
		return videos.values();
	}


	@RequestMapping(value=VIDEO_SVC_PATH, method=RequestMethod.POST)
	public @ResponseBody Video addVideo(@RequestBody Video v) {
		// TODO Auto-generated method stub
		Video tempV = save(v);
		long newId = tempV.getId();
		String videoUrl = getDataUrl(newId);
		v.setDataUrl(videoUrl);
		return v;
	}

	////  Java Method given by Dr Jules to set unique id
	private void checkAndSetId(Video entity) {
		if(entity.getId() == 0){
			entity.setId(currentId.incrementAndGet());
		}
	}
	
  	public Video save(Video entity) {
		checkAndSetId(entity);
		videos.put((Long) entity.getId(), entity);
		return entity;
	}
	
	
	////  Java Method given by Dr Jules to create a data url from the video id.
    private String getDataUrl(long videoId){
        String url = getUrlBaseForLocalServer() + "/video/" + videoId + "/data";
        return url;
    }

 	private String getUrlBaseForLocalServer() {
	   HttpServletRequest request = 
	       ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
	   String base = 
	      "http://"+request.getServerName() 
	      + ((request.getServerPort() != 80) ? ":"+request.getServerPort() : "");
	   return base;
	}
	

	@RequestMapping(value = VIDEO_DATA_PATH, method = RequestMethod.POST)
	public @ResponseBody
	VideoStatus setVideoData(@PathVariable("id") long id,
			@RequestPart("data") MultipartFile videoData,
			HttpServletResponse response) throws IOException {
		// TODO Auto-generated method stub

		VideoFileManager vMgr = VideoFileManager.get();
		Video v = videos.get(id);
		
		if ( v != null  ) {
			vMgr.saveVideoData(v, videoData.getInputStream());
			return new VideoStatus(VideoState.READY);
		} else {
			response.setStatus(HttpServletResponse.SC_NOT_FOUND);
			return null;
		}
	}


	@RequestMapping(value = VIDEO_DATA_PATH, method = RequestMethod.GET)
	public void getData(@PathVariable("id") long id,
			HttpServletResponse response) throws IOException {
		// TODO Auto-generated method stub

		VideoFileManager vMgr = VideoFileManager.get();
		Video v = videos.get(id);
		if ( v != null ) {
			vMgr.copyVideoData(v, response.getOutputStream());
		} else {
			response.setStatus(HttpServletResponse.SC_NOT_FOUND);
		}
	}
}
